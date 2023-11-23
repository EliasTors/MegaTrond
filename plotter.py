import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the CSV file into a pandas dataframe with optimized parameters
df = pd.read_csv('test.csv', parse_dates=['datetime'], dtype={'temp': float, 'pressure': float, 'humidity': float, 'gas': float, 'lyd': float, 'lys': float})

# Plot the data using Seaborn
sns.set(style="darkgrid", palette="muted")

plt.figure(figsize=(8, 6))

plt.subplot(3, 2, 1)
sns.lineplot(x='datetime', y='temp', data=df)
plt.title('Temperature')

plt.subplot(3, 2, 2)
sns.lineplot(x='datetime', y='pressure', data=df)
plt.title('Pressure')

plt.subplot(3, 2, 3)
sns.lineplot(x='datetime', y='humidity', data=df)
plt.title('Humidity')

plt.subplot(3, 2, 4)
sns.lineplot(x='datetime', y='gas', data=df)
plt.title('Gas')

plt.subplot(3, 2, 5)
sns.lineplot(x='datetime', y='lyd', data=df)
plt.title('Sound')

plt.subplot(3, 2, 6)
sns.lineplot(x='datetime', y='lys', data=df)
plt.title('Light')

plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()
