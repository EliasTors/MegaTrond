import sqlite3
import serial
import time
from datetime import datetime

# Open serial connection (replace '/dev/ttyUSB0' with your device path)
ser = serial.Serial('/dev/ttyACM0', 600)

# Wait for the Arduino to initialize
time.sleep(2)

# Connect to the SQLite database
conn = sqlite3.connect('serial_data.db')
cursor = conn.cursor()

# Create a table for the data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        datetime TEXT,
        line TEXT
    )
''')

try:
    while True:
        if ser.in_waiting:
            # Read a line from the serial connection
            line = ser.readline()

            try:
                line = line.decode('utf-8').rstrip()
            except UnicodeDecodeError:
                print("Could not decode line, skipping...")
                line = "error"

            now = datetime.now().isoformat()

            # Insert the line and datetime into the database
            cursor.execute('INSERT INTO data VALUES (?, ?)', (now, line))

            # Commit the changes
            conn.commit()

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    conn.close()