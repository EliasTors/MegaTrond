import serial
import time
import csv
from datetime import datetime

# Open serial connection (replace '/dev/ttyACM0' with your device path)
ser = serial.Serial('/dev/ttyACM0', 9600)

# Wait for the Arduino to initialize
time.sleep(2)

# Open a CSV file in write mode
with open('serial_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    while True:
        if ser.in_waiting:
            # Read a line from the serial connection
            line = ser.readline().decode('utf-8').rstrip()

            # Get the current datetime
            now = datetime.now()

            # Write the line and datetime to the CSV file
            writer.writerow([line, now])

            # Flush the file to force the data to be written to disk
            file.flush()