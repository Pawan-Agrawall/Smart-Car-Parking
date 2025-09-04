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

# Ensure table exists
cursor.execute('''CREATE TABLE IF NOT EXISTS entry (number TEXT, time TEXT, status INTEGER)''')
conn.commit()

def recognize_plate_from_frame(frame):
    global processing, ultrasonic_enabled
    processing = True

    img_name = "temp_frame.jpg"
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
                # Check available slots before allowing entry
                cursor.execute("SELECT COUNT(*) FROM entry WHERE status = 1")
                count_in = cursor.fetchone()[0]

                if count_in < total_slots:  # There's space for more cars
                    if plate_number not in seen_plates:
                        seen_plates.add(plate_number)
                        print(f"✅ Valid Plate: {plate_number}")
                    
                        # INSERT new entry into DB with status = 1
                        cursor.execute("INSERT INTO entry (number, time, status) VALUES (?, datetime('now'), 1)", (plate_number,))
                        conn.commit()
                        print(f"🅿️ Entry recorded for {plate_number}. Available slots: {total_slots - count_in - 1}")
                    
                        # Reduce available slots
                        arduino.write(f"Available slots: {total_slots - count_in - 1}\n".encode())
                    else:
                        print(f"⚠️ Duplicate Plate: {plate_number}")
                else:
                    print("❌ Parking full, car denied entry.")
                    # If parking is full, deny entry and show available slot count
                    arduino.write(f"Parking Full! Available slots: {total_slots - count_in}\n".encode())
            
                ultrasonic_enabled = True
                arduino.write(b"start_ultrasonic\n")
            else:
                print(f"⚠️ Invalid Plate: {plate_number}")
                ultrasonic_enabled = False
                arduino.write(b"stop_ultrasonic\n")
        else:
            print("⚠️ No plate detected.")
            ultrasonic_enabled = False
            arduino.write(b"stop_ultrasonic\n")

    except Exception as e:
        print(f"❌ Error: {e}")

    processing = False

def live_plate_scanner():
    cap = cv2.VideoCapture(MOBILE_CAM_URL)
    if not cap.isOpened():
        print("❌ Could not open camera.")
        return

    print("📡 Scanning started. Press ESC to stop.")
    frame_counter = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame read failed.")
            break

        cv2.imshow("ANPR Feed", frame)
        frame_counter += 1

        if frame_counter % 5 == 0 and not processing:
            threading.Thread(target=recognize_plate_from_frame, args=(frame,)).start()

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

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

def send_available_slots():
    while True:
        cursor.execute("SELECT COUNT(*) FROM entry WHERE status = 1")
        count_in = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM entry WHERE status = 0")
        count_out = cursor.fetchone()[0]

        available = total_slots - (count_in - count_out)
        arduino.write(f"{available}\n".encode())
        if available > 0 and available < total_slots:
            print(f"📤 Available slots sent: {available}")
        else:
            print("Not Available")

        time.sleep(5)

# Start threads
threading.Thread(target=monitor_ultrasonic, daemon=True).start()
threading.Thread(target=send_available_slots, daemon=True).start()

# Run plate scanner
live_plate_scanner()
