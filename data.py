import sqlite3
import pandas as pd

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

        # Replace "\n\n" with "\n" and '""' with ''
        content = [line.replace('\n\n', '\n').replace('"', '') for line in content]

        with open(csv_file, 'w') as file:
            file.writelines(content)
        