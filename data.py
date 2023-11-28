import sqlite3
import pandas as pd
from datetime import timedelta
from datetime import datetime
import pandas as pd


class dataHandler:
    def removeQ(filepath):
        with open(filepath, 'r') as file:
            content = file.read()

        content = content.replace('"', '')

        with open(filepath, 'w') as file:
            file.write(content)
    
    def sql_to_csv(db_file, csv_file="data.csv", table="data"):
        # Connect to the database and fetch data
        with sqlite3.connect(db_file) as con:
            query = f"SELECT datetime, line FROM {table}"
            df = pd.read_sql_query(query, con)

        # Write data to CSV
        df.to_csv(csv_file, index=False)

        # Read the CSV file
        with open(csv_file, 'r') as file:
            content = file.readlines()

        # Modify the first line
        content[0] = "datetime,temp,pressure,humidity,gas,lyd,lys\n"

        # Filter and modify content
        content = [
            line.replace('\n\n', '\n').replace('"', '')
            for line in content
            if "error" not in line
            and "Temp,Pressure, humidity, gas, lyd, lys" not in line
            and len(line.split(',')) == 7
        ]

        # Write the modified content back to the CSV file
        with open(csv_file, 'w') as file:
            file.writelines(content)
            
    def shift_datetime(sqlite_file, start_time, table_name="data"):
        # Convert the start_time string to a datetime object
        start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")

        # Connect to the SQLite database and fetch all rows from the table
        with sqlite3.connect(sqlite_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Get the first datetime value in the table
            first_datetime = datetime.strptime(rows[0][0], "%Y-%m-%dT%H:%M:%S.%f")

            # Iterate through the rows and update the datetime values
            for row in rows:
                time_diff = datetime.strptime(row[0], "%Y-%m-%dT%H:%M:%S.%f") - first_datetime
                new_datetime = start_datetime + time_diff
                new_datetime_str = new_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")

                # Update the row with the new datetime value
                cursor.execute(f"UPDATE {table_name} SET datetime = ? WHERE line = ?", (new_datetime_str, row[1]))

            # Commit the changes
            conn.commit()

    def clean_csv(csv_file, out):
        # Read the CSV file
        with open (csv_file, 'r') as file:
            content = file.readlines()

        # Modify the column names
        #df.columns = ['datetime', 'temp', 'pressure', 'humidity', 'gas', 'lyd', 'lys']
        
        
    # Filter and modify content
        content = [
        line.replace('\n\n', '\n').replace('"', '')
        for line in content
        if "error" not in line
        and "Temp,Pressure, humidity, gas, lyd, lys" not in line
        and len(line.split(',')) == 7
        ]
        
        
        # Write the modified data back to the CSV file
        with open(out, 'w') as file:
            file.writelines(content)

class estemation:
    def extrapolate_data(csv_file, start_datetime, end_datetime):
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Convert datetime column to datetime type with the specified format
        df['datetime'] = pd.to_datetime(df['datetime'], format="%Y-%m-%d %H:%M:%S.%f")

        # Convert start_datetime and end_datetime to datetime type with the specified format
        start_datetime = pd.to_datetime(start_datetime, format="%Y-%m-%d %H:%M:%S.%f")
        end_datetime = pd.to_datetime(end_datetime, format="%Y-%m-%d %H:%M:%S.%f")

        # Filter data within the specified datetime range
        filtered_df = df[(df['datetime'] >= start_datetime) & (df['datetime'] <= end_datetime)]

        # Extrapolate data using interpolation
        extrapolated_df = filtered_df.interpolate(method='linear')

        return extrapolated_df
