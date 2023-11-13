
import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas dataframe
df = pd.read_csv('serial_data_2023-11-13_14-09-31.csv')

# Extract the data columns
temp = df['Temp']
pressure = df['Pressure']
humidity = df['humidity']
gas = df['gas']
lyd = df['lyd']
lys = df['lys']

# Plot the data
plt.figure(figsize=(8, 6))

plt.subplot(3, 2, 1)
plt.plot(temp, label='Temperature')
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(pressure, label='Pressure')
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(humidity, label='Humidity')
plt.legend()

plt.subplot(3, 2, 4)
plt.plot(gas, label='Gas')
plt.legend()

plt.subplot(3, 2, 5)
plt.plot(lyd, label='Sound')
plt.legend()

plt.subplot(3, 2, 6)
plt.plot(lys, label='Light')
plt.legend()

plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()
