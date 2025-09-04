import sqlite3

# Connect to the database
conn = sqlite3.connect('parking.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM entry")
# cursor.execute("DROP TABLE entry")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("deleted")
