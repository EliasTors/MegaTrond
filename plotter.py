import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime


class plotter:
    def plot_data(self, filenames, interval):
        dataframes = []
        for filename in filenames:
            df = pd.read_csv(filename, parse_dates=['datetime'], date_parser=lambda x: pd.to_datetime(x, format="%Y-%m-%dT%H:%M:%S.%f"))
            df['date'] = df['datetime'].dt.date
            df['time'] = df['datetime'].apply(lambda x: datetime.datetime.combine(datetime.date.today(), x.time()))
            dataframes.append(df)
            
        data = pd.concat(dataframes, ignore_index=True)
        
        print("Unique dates in CSV file:", data['date'].unique())
    
        #Dato til rom:
        room_codes = {
                    datetime.date(2023, 11, 21): 'R04', 
                    datetime.date(2023, 11, 20): 'R03',
                    datetime.date(2023, 11, 24): 'FYS'}
        data['room'] = data['date'].map(room_codes)

        fig, axs = plt.subplots(6, figsize=(10, 20))

        rooms = data['room'].unique()

        for room in rooms:
            data_room = data[data['room'] == room]
            data_room = data_room.set_index('time').resample(interval).mean().reset_index()
            axs[0].plot(data_room['time'], data_room['temp'], label=f'Temperature in {room}')
            axs[1].plot(data_room['time'], data_room['pressure'], label=f'Pressure in {room}')
            axs[2].plot(data_room['time'], data_room['humidity'], label=f'Humidity in {room}')
            axs[3].plot(data_room['time'], data_room['gas'], label=f'Gas in {room}')
            axs[4].plot(data_room['time'], data_room['lyd'], label=f'Lyd in {room}')
            axs[5].plot(data_room['time'], data_room['lys'], label=f'Lys in {room}')

        for i, label in enumerate(['Temperature (°C)', 'Pressure (hPa)', 'Humidity (%)', 'Gas', 'Lyd', 'Lys']):
            axs[i].set_xlabel('Time')
            axs[i].set_ylabel(label)
            axs[i].set_title(f'{label} over Time')
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            axs[i].legend()

        plt.tight_layout()
        plt.show()
