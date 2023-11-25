import sqlite3
import pandas as pd
from datetime import timedelta

class dataHandler:
    def removeQ(filepath):
        with open(filepath, 'r') as file:
            content = file.read()

        content = content.replace('"', '')

        with open(filepath, 'w') as file:
            file.write(content)
    
    def sql_to_csv(db_file, csv_file="data.csv"):
        con = sqlite3.connect(db_file)
        query = "SELECT datetime, line FROM data"
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
    def shift_datetime(filepath, shift):
        # Connect to the SQLite database
        conn = sqlite3.connect(filepath)

        # Read the data into a pandas DataFrame
        df = pd.read_sql_query("SELECT * FROM data", conn)

        # Create a copy of the DataFrame to avoid modifying the original data
        df_copy = df.copy()

        # Convert the first column to datetime if it's not already
        df_copy[df_copy.columns[0]] = pd.to_datetime(df_copy[df_copy.columns[0]])

        # Shift the datetime column 83 hours forward
        df_copy[df_copy.columns[0]] = df_copy[df_copy.columns[0]] + timedelta(hours=shift)

        # Write the updated DataFrame back to the SQLite database
        df_copy.to_sql('data', conn, if_exists='replace', index=False)

        # Close the connection
        conn.close()
