import sqlite3
from datetime import datetime

# Database name
DB_NAME = "parking.db"

# Step 1: Create the database and table if not exist
def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE entry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT NOT NULL,
    time TEXT NOT NULL,
    status INTEGER NOT NULL
    );

    """)
    
    conn.commit()
    conn.close()
    print("✅ Database and table setup complete.")

# Step 2: Insert data into the entry table
def insert_plate_to_db(plate_number, status=1):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        in_time = datetime.now()
        cursor.execute("""
            INSERT INTO entry (number, time, status)
            VALUES (?, ?, ?)
        """, (plate_number, in_time, status))
        
        conn.commit()
        conn.close()
        print(f"📥 Plate '{plate_number}' inserted at {in_time}.")
    except Exception as e:
        print(f"❌ Failed to insert into DB: {e}")

# Example usage
if __name__ == "__main__":
    setup_database()
    
    # Simulated plate detection
    insert_plate_to_db("RJ14AB1234", status=1)
    insert_plate_to_db("DL12CD4321", status=0)
