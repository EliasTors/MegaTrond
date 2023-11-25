import sqlite3
import pandas as pd
from datetime import timedelta
from datetime import datetime


class dataHandler:
    def removeQ(filepath):
        with open(filepath, 'r') as file:
            content = file.read()

        content = content.replace('"', '')

        with open(filepath, 'w') as file:
            file.write(content)
    
    def sql_to_csv(db_file, csv_file="data.csv", table="data"):
        con = sqlite3.connect(db_file)
        query = f"SELECT datetime, line FROM {table}"
        df = pd.read_sql_query(query, con)
        df.to_csv(csv_file, index=False)
        con.close()

        # Open the CSV file and replace all "/n/n" with "/n"
        with open(csv_file, 'r') as file:
            content = file.readlines()

        # Modify the first line to "datetime,temp,pressure,humidity,gas,lyd,lys"
        content[0] = "datetime,temp,pressure,humidity,gas,lyd,lys\n"

        # Remove lines containing "error" or "Temp,Pressure, humidity, gas, lyd, lys"
        content = [line for line in content if "error" not in line and "Temp,Pressure, humidity, gas, lyd, lys" not in line]

        # Remove lines that are not complete (do not contain all the expected columns)
        content = [line for line in content if len(line.split(',')) == 7]

        # Replace "\n\n" with "\n" and '""' with ''
        content = [line.replace('\n\n', '\n').replace('"', '') for line in content]

        with open(csv_file, 'w') as file:
            file.writelines(content)

class dataFixer:
    def shift_datetime(sqlite_file, start_time, table_name="data"):
        # Convert the start_time string to a datetime object
        start_datetime = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")

        # Connect to the SQLite database
        conn = sqlite3.connect(sqlite_file)
        cursor = conn.cursor()

        # Fetch all rows from the table
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

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        
        
        
        '''
        # Connect to the SQLite database
        conn = sqlite3.connect(filepath)

        # Read the data into a pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM data", conn)

        # Create a copy of the DataFrame to avoid modifying the original data
        df_copy = df.copy()

        # Convert the first column to datetime if it's not already
        df_copy[df_copy.columns[0]] = pd.to_datetime(df_copy[df_copy.columns[0]], format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')

        # Calculate the time difference between the start datetime and the first datetime in the DataFrame
        start_datetime = pd.to_datetime(start_datetime)
        
        # Calculate the time difference between the start datetime and the first datetime in the DataFrame
        time_diff = start_datetime - df_copy[df_copy.columns[0]].min()

        # Shift the datetime column by the calculated time difference
        df_copy[df_copy.columns[0]] = df_copy[df_copy.columns[0]] + time_diff

        # Write the updated DataFrame to a new table in the SQLite database
        df_copy.to_sql('shifted_data', conn, if_exists='replace', index=False)

        # Close the connection
        conn.close()
'''