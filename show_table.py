import sqlite3

# Database name
DB_NAME = "parking.db"

def view_entry_table():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM entry")
        rows = cursor.fetchall()

        if rows:
            print("📋 All Entries in 'entry' Table:")
            print("-" * 50)
            for row in rows:
                print(f"ID: {row[0]} | Number: {row[1]} | In-Time: {row[2]} | Status: {row[3]}")
        else:
            print("⚠️ No entries found in the 'entry' table.")
        
        conn.close()
    except Exception as e:
        print(f"❌ Error reading database: {e}")

# Run the function
if __name__ == "__main__":
    view_entry_table()
