import serial
import cv2
import requests
import threading
import time
import sqlite3

# Plate Recognizer API
# API_URL = 'https://api.platerecognizer.com/v1/plate-reader/'
# API_TOKEN = '9acbbf907a2fc37c8f267b76e1508a321e422eb4'
# MOBILE_CAM_URL = 'http://192.168.1.37:8080/video'

# Serial & DB setup
arduino = serial.Serial('COM5', 9600)
time.sleep(2)
conn = sqlite3.connect('parking.db', check_same_thread=False)
cursor = conn.cursor()

seen_plates = set()
processing = False
ultrasonic_enabled = False
total_slots = 3




def recognize_plate(frame):
    global processing, ultrasonic_enabled
    processing = True
    img_name = "exit_frame.jpg"
    cv2.imwrite(img_name, frame)

    try:
        with open(img_name, 'rb') as img_file:
            response = requests.post(
                API_URL,
                files={'upload': img_file},
                headers={'Authorization': f'Token {API_TOKEN}'}
            )

        result = response.json()
        if 'results' in result and len(result['results']) > 0:
            plate_number = result['results'][0]['plate'].upper()

            if len(plate_number) == 10:
                cursor.execute("SELECT status FROM entry WHERE number = ? ORDER BY time DESC LIMIT 1", (plate_number,))
                status_record = cursor.fetchone()

                if status_record:
                    last_status = status_record[0]
                    if last_status == 1:
                        cursor.execute("INSERT INTO entry (number, time, status) VALUES (?, datetime('now'), 0)", (plate_number,))
                        conn.commit()
                        print(f"✅ Valid Plate: {plate_number}")
                        print(f"🅿️ Exit recorded for {plate_number}") 
                    else:
                        print(f"⚠️ Car {plate_number} has already exited.")                 
                else:
                    print(f"❌ No entry record found for {plate_number}.")

                ultrasonic_enabled = True
                arduino.write(b"start_ultrasonic\n")    
            else:
                print(f"⚠️ Invalid Plate Length: {plate_number}")
                ultrasonic_enabled = False
                arduino.write(b"stop_ultrasonic\n")
        else:
            print("⚠️ No plate detected.")
            ultrasonic_enabled = False
            arduino.write(b"stop_ultrasonic\n")

    except Exception as e:
        print(f"❌ Error: {e}")
    processing = False

def monitor_ultrasonic():
    global ultrasonic_enabled
    while True:
        if ultrasonic_enabled:
            arduino.write(b"trigger_ultrasonic\n")
            if arduino.in_waiting > 0:
                try:
                    distance = arduino.readline().decode('utf-8').strip()
                    print(f"📏 Distance: {distance} cm")
                except:
                    pass
        else:
            arduino.write(b"stop_ultrasonic\n")

        time.sleep(0.1)


def exit_scanner():
    cap = cv2.VideoCapture(MOBILE_CAM_URL)
    if not cap.isOpened():
        print("❌ Could not open camera.")
        return

    print("📡 Exit scanner started. Press ESC to stop.")
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame read failed.")
            break

        cv2.imshow("Exit Camera", frame)
        frame_counter += 1

        if frame_counter % 5 == 0 and not processing:
            threading.Thread(target=recognize_plate, args=(frame,)).start()

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def send_available_slots():
    while True:
        # Fetch only latest status per vehicle
        cursor.execute("""
            SELECT number, status
            FROM entry
            WHERE time IN (
                SELECT MAX(time)
                FROM entry
                GROUP BY number
            )
        """)
        records = cursor.fetchall()
        inside_count = sum(1 for _, status in records if status == 1)
        available = total_slots - inside_count

        arduino.write(f"{available}\n".encode())
        if available > 0:
            print(f"📤 Available slots sent: {available}")
        else:
            print("🚫 Not Available")

        time.sleep(5)


threading.Thread(target=monitor_ultrasonic, daemon=True).start()
threading.Thread(target=send_available_slots, daemon=True).start()

# Run the scanner
exit_scanner()
