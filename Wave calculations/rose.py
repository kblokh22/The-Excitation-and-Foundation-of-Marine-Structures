import pandas as pd
import matplotlib.pyplot as plt
from windrose import WindroseAxes
import matplotlib.colors as colors
import matplotlib.ticker as mtick
import numpy as np

def truncate_colormap(color, minval=0.0, maxval=1.0, n=100):
    cmap = plt.colormaps.get_cmap(color)
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

df = pd.read_excel("Weather data/Vejrdata 2018-2025.xlsx")

date = pd.to_datetime(df['Column1'].iloc[2:].values, format='%d/%m/%Y %H:%M:%S')
water_level = df['Column2'].iloc[2:].astype(float)
wind_speed = df['Column3'].iloc[2:].astype(float)
gust_speed = df['Column4'].iloc[2:].astype(float)
wind_direction = df['Column5'].iloc[2:].astype(float)
air_temperature = df['Column6'].iloc[2:].astype(float)
mid_wave = df['Column7'].iloc[2:].astype(float)
max_wave = df['Column8'].iloc[2:].astype(float)
wave_direction = df['Column10'].iloc[2:].astype(float)
current_direction = df['Column11'].iloc[2:].astype(float)
current_speed = df['Column12'].iloc[2:].astype(float)
sea_temperature = df['Column13'].iloc[2:].astype(float)

fig = plt.figure(figsize=(8, 8))
ax = WindroseAxes.from_ax(fig=fig)
cmap = truncate_colormap('PuBuGn', 0.1, 0.9)

ax.bar(wave_direction, mid_wave, normed=True, opening=0.8, cmap=cmap, nsector=32)

fmt = '%.0f%%'
yticks = mtick.FormatStrFormatter(fmt)
ax.yaxis.set_major_formatter(yticks)

ax.set_legend(title="Significant wave height (m)", loc='lower right', decimal_places=1)
plt.show()


