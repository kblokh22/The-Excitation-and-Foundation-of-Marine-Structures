import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import label

years = np.arange(2013,2019)

dates = []
water_levels = []
mid_waves = []
max_waves = []

for year in years:
    df = pd.read_excel("Weather data/Samlet vejrdata 2013.2019-NK.xlsx",sheet_name=f'{year}')

    dates.extend(df['Tidspunkt'].iloc[1:])
    water_levels.extend(df['Vandstand [m]'].iloc[1:])
    mid_waves.extend(df['Mid. bølg [m]'].iloc[1:])
    max_waves.extend(df['Max. bølg. [m]'].iloc[1:])

df = pd.read_excel("Weather data/Vejrdata 2018-2025.xlsx")

date = pd.to_datetime(df['Column1'].iloc[2:].values, format='%d/%m/%Y %H:%M:%S')
water_level = df['Column2'].iloc[2:].astype(float)
mid_wave = df['Column7'].iloc[2:].astype(float)
max_wave = df['Column8'].iloc[2:].astype(float)

dates.extend(date)
water_levels.extend(water_level)
mid_waves.extend(mid_wave)
max_waves.extend(max_wave)

dates = np.array(dates)
water_levels = np.array(water_levels)
mid_waves = np.array(mid_waves)
max_waves = np.array(max_waves)
mid_waves[mid_waves > 6] = np.nan

# Filter out NaN values in max waves
mask = ~np.isnan(mid_waves)
filtered_dates = dates[mask]
filtered_max_waves = mid_waves[mask]

plt.figure()
plt.plot(filtered_dates, filtered_max_waves)
plt.xlabel('Date')
plt.ylabel('Significant wave height [m]')
plt.title('Water level over time')
plt.show()