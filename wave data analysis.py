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

print(f'Number of dates: {len(dates)}')
print(f'Number of water levels: {len(water_levels)}')
print(f'Number of mid waves: {len(mid_waves)}')
print(f'Number of max waves: {len(max_waves)}')

print(type(dates[0]))

plt.figure()
plt.plot(dates, water_levels)
plt.show()