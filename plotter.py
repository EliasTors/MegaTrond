import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a pandas dataframe
df = pd.read_csv('test.csv')

# Extract the data columns
datetime = df['datetime']
temp = df['temp']
pressure = df['pressure']
humidity = df['humidity']
gas = df['gas']
lyd = df['lyd']
lys = df['lys']

# Plot the data
plt.figure(figsize=(8, 6))

plt.subplot(3, 2, 1)
plt.plot(datetime, temp, label='Temperature', alpha=0.7)
plt.legend()

plt.subplot(3, 2, 2)
plt.plot(datetime, pressure, label='Pressure', alpha=0.7)
plt.legend()

plt.subplot(3, 2, 3)
plt.plot(datetime, humidity, label='Humidity', alpha=0.7)
plt.legend()

plt.subplot(3, 2, 4)
plt.plot(datetime, gas, label='Gas')
plt.legend()

plt.subplot(3, 2, 5)
plt.plot(datetime, lyd, label='Sound')
plt.legend()

plt.subplot(3, 2, 6)
plt.plot(datetime, lys, label='Light')
plt.legend()

plt.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()
