import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

years = np.arange(2013,2019)

dates = []
water_levels = []
mid_waves = []
max_waves = []

for year in years:
    df = pd.read_excel("Weather data/Samlet vejrdata 2013.2019-NK.xlsx",sheet_name=f'{year}')
    date = df['Tidspunkt']
    water_level = df['Vandstand [m]']
    mid_wave = df['Mid. bølg [m]']
    max_wave = df['Max. bølg. [m]']
    dates.extend(date.iloc[1:])
    water_levels.extend(water_level.iloc[1:])
    mid_waves.extend(mid_wave.iloc[1:])
    max_waves.extend(max_wave.iloc[1:])

df = pd.read_excel("Weather data/Vejrdata 2018-2025.xlsx")

date = pd.to_datetime(df['Column1'].iloc[2:].values, format='%d/%m/%Y %H:%M:%S')
water_level = df['Column2'].iloc[2:].astype(float)
mid_wave = df['Column7'].iloc[2:].astype(float)
max_wave = df['Column8'].iloc[2:].astype(float)

dates.extend(date)
water_levels.extend(water_level)
mid_waves.extend(mid_wave)
max_waves.extend(max_wave)

plt.figure()
plt.plot(dates, water_levels)
plt.xlabel('Date')
plt.ylabel('Water level [m]')
plt.title('Water level over time')
plt.show()