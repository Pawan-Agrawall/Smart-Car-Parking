# Smart Car Parking System

## Overview
The Smart Car Parking System is an IoT-based project designed to automate parking management.  
It combines **Python-based software**, **Arduino-controlled hardware**, and an **API for vehicle number plate recognition**.

---

## Features
- Automatic gate opening/closing via motor
- Real-time parking slot detection (ultrasonic sensors)
- Display of parking slot availability
- Vehicle number plate fetching via API
- Database-driven entry and exit logging

---

## Project Structure
Smart-Car-Parking/
├── hardware/ # Arduino code and circuit diagrams
├── software/ # Python scripts and database
├── videos/ # Demo videos
└── README.md


| Path                 | Description                     |
|----------------------|---------------------------------|
| `hardware/`          | Contains Arduino/circuit files  |
| `software/`          | Python scripts & DB logic       |
| `videos/`            | Project demonstration videos    |

---

## Hardware Used
- Arduino Board (e.g., Arduino Uno)
- DC/Servo Motor (for gate)
- Ultrasonic Sensors (for slot detection)
- LCD/LED Display (for parking status)
- API Integration (license plate recognition)

---

## Installation & Setup
1. Clone/download this repository.
2. Connect the hardware (Arduino, sensors, motor, display).
3. Upload Arduino sketch to the board (if applicable).
4. Install Python dependencies:
   ```bash
   pip install pillow requests
Ensure parking.db exists or run database.py to initialize.

Running the Project
Run the following scripts:

python software/entry_logic.py   # For vehicle entry
python software/exit_logic.py    # For vehicle exit
python software/show_table.py    # To see parking table

## Demonstration Videos
▶ Code Working Demo
<video src="videos/code_demo.mp4" controls width="700"></video>

▶ Hardware Working Demo
<video src="videos/hardware_demo.mp4" controls width="700"></video>


Author
Pawan Agrawal
B.Tech (Hons), GLA University

License
Educational use only. You may modify and use with attribution.

---

### 📌 Next steps (you need to do manually on your laptop)
1. Create a folder called `Smart-Car-Parking`.  
2. Move all your Python files, DB, and images into a `software` subfolder.  
3. Create a `hardware` folder (add Arduino `.ino` file and optional circuit diagram if you have one).  
4. Create a `videos` folder and put your two `.mp4` videos there:
   - `code_demo.mp4`  
   - `hardware_demo.mp4`  
5. Save the above README.md in the main `Smart-Car-Parking` folder.  

---


