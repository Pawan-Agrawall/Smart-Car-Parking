# 🚗 Smart Car Parking – IoT-Powered Automated Parking Management

An intelligent parking system that makes parking **efficient, automated, and user-friendly** using a combination of **Python software**, **Arduino hardware**, and **API integration**.

---

## 🚀 Overview

Smart Car Parking is an end-to-end IoT project that revolutionizes how vehicles are parked:

- **Automated gate control** using motors
- **Real-time slot detection** via ultrasonic sensors
- **Automatic number plate fetching** through API
- **Database-driven logging** for entry/exit
- **User interface** to monitor and manage parking data

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🅿️ **Automatic Parking Slot Detection** | Ultrasonic sensors track vehicle presence in slots |
| 🚧 **Motorized Gate Control** | Arduino-controlled motor opens/closes the gate |
| 🖥 **LCD/LED Display** | Shows live parking availability |
| 🗄 **SQLite Database** | Logs vehicle entry and exit details |
| 🔢 **Number Plate Recognition** | API fetches and records vehicle plate numbers |
| 🧩 **Modular Design** | Easily expandable for more slots and more gates |
| 🖥 **Python Interface** | Scripts to manage and view parking data |

---


## 🎥 Demo

> 📹 **Code Working Demo**  
> <video src="videos/code_demo.mp4" controls width="700"></video>  
>
> 🚗 **Hardware Working Demo**  
> <video src="videos/hardware_demo.mp4" controls width="700"></video>

---

## 🏗️ Architecture

### How It Works

1. **Vehicle Arrives** → Ultrasonic sensor detects presence  
2. **License Plate Recognition** → API fetches the vehicle number  
3. **Gate Control** → Arduino triggers motor to open/close gate  
4. **Data Logging** → Python scripts update SQLite database  
5. **User Monitoring** → Python interface shows current parking table and history

### Tech Stack

| Component | Technology |
|-----------|------------|
| **Hardware Control** | Arduino Uno |
| **Sensors** | Ultrasonic sensors |
| **Motor** | DC/Servo motor for gate |
| **Display** | LCD/LED display |
| **Backend Logic** | Python |
| **Database** | SQLite3 |
| **Number Plate API** | External REST API |
| **UI/Reports** | Python scripts with image frames |

---

## 📂 Project Structure

Smart-Car-Parking/
├──database.py
│ ├── entry_logic.py
│ ├── exit_logic.py
│ ├── delete.py
│ ├── show_table.py
│ ├── parking.db
│ ├── exit_frame.jpg
│ └── temp_frame.jpg
├── videos/
│ ├── code_demo.mp4 # Code working demo
│ └── hardware_demo.mp4 # Hardware working demo
└── README.md




---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Arduino IDE (for uploading hardware code)
- Ultrasonic sensors, motor, LCD display connected to Arduino

### Installation

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/smart-car-parking
   cd smart-car-parking
Set up Python environment (optional)



python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
Install dependencies



pip install pillow requests
Connect hardware

Upload hardware/hardware_code.ino to Arduino

Ensure sensors, motor, and display are wired correctly

Run the application



python software/entry_logic.py   # Handle vehicle entry
python software/exit_logic.py    # Handle vehicle exit
python software/show_table.py    # View parking table
## 📋 Usage Examples
Automatic logging when a vehicle enters/exits

Manual database cleaning via delete.py

Displaying current parking availability on LCD display

Expanding for multiple slots with additional sensors and DB entries

## 🤝 Contributing
We welcome contributions! Please:

Fork the repository

Create a branch (git checkout -b feature/upgrade-gate)

Commit changes (git commit -m 'Add upgraded gate control')

Push (git push origin feature/upgrade-gate)

Open a Pull Request

👨‍💻 Author
Pawan Agrawal – GitHub Profile

<div align="center">
Made with ❤️ for smarter, automated parking solutions.
⭐ If this project helped you, please give it a star!

</div> ```
