import pandas as pd

# Read the CSV file
df = pd.read_csv('day one.5.csv')

# Convert the "date" column to datetime format
df['datetime'] = pd.to_datetime(df['datetime'])

# Push the date 86 hours forward
df['datetime'] = df['datetime'] + pd.Timedelta(hours=+24)

# Save the modified DataFrame to a new CSV file
df.to_csv('modified date.csv', index=False)
