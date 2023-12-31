from io import StringIO
import sqlite3
import pandas as pd
from datetime import timedelta
from datetime import datetime


class dataHandler:
    def removeQ(filepath):
        """
        Remove all occurrences of double quotes from the file at the given filepath.

        Args:
            filepath (str): The path to the file.

        Returns:
            None
        """
        with open(filepath, 'r') as file:
            content = file.read()

        content = content.replace('"', '')

        with open(filepath, 'w') as file:
            file.write(content)
    
    def sql_to_csv(db_file, csv_file="data.csv", table="data"):
        """
        Export data from an SQLite database table to a CSV file.

        Parameters:
        - db_file (str): The path to the SQLite database file.
        - csv_file (str): The path to the output CSV file (default: "data.csv").
        - table (str): The name of the table in the database to export (default: "data").

        Returns:
        None
        """
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
        """
        Shifts the datetime values in a SQLite table by a specified start time.

        Args:
            sqlite_file (str): The path to the SQLite database file.
            start_time (str): The start time in the format "%Y-%m-%dT%H:%M:%S".
            table_name (str, optional): The name of the table in the SQLite database. Defaults to "data".

        Returns:
            None
        """
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
        """
        Cleans the given CSV file by removing unwanted lines and modifying the content.

        Args:
            csv_file (str): The path to the input CSV file.
            out (str): The path to the output CSV file.

        Returns:
            None
        """
        # Read the CSV file
        with open(csv_file, 'r') as file:
            content = file.readlines()

        # Modify the column names
        # df.columns = ['datetime', 'temp', 'pressure', 'humidity', 'gas', 'lyd', 'lys']

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
    def fill_time_gaps(csv_data, freq='T'):
        """
        Fill time gaps in the CSV data by resampling it at a regular interval.

        Parameters:
        csv_data (str): The path to the CSV file containing the data.
        freq (str, optional): The frequency at which to resample the data. Defaults to 'T' (every minute).

        Returns:
        pandas.DataFrame: The resampled and filled DataFrame.
        """
        # Read the CSV data and convert 'datetime' column to datetime
        df = pd.read_csv(csv_data, parse_dates=['datetime'], date_parser=lambda x: pd.to_datetime(x, format="%Y-%m-%d %H:%M:%S.%f"))

        # Set 'datetime' as the index
        df.set_index('datetime', inplace=True)

        # Resample the data at a regular interval (e.g., every second) and fill gaps in the data
        df_filled = df.resample(freq).mean().ffill().reset_index()

        return df_filled




