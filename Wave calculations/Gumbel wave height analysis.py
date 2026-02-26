import pandas as pd
import numpy as np
from scipy import stats
from scipy.ndimage import label, maximum_position
import matplotlib.pyplot as plt
from helper_functions import *

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

mid_waves = np.where(mid_waves > 5, np.nan, mid_waves)

# Filter out NaN values in mid waves
mask = ~np.isnan(mid_waves)
filtered_dates = dates[mask]
filtered_waves = mid_waves[mask]

# Find peaks in filtered waves
mask = filtered_waves > 3.2
labels, num_features = label(mask)
peak_indices = maximum_position(filtered_waves, labels, range(1, num_features + 1))

# Extract peak values
peak_indices = [idx[0] for idx in peak_indices]
peak_values = filtered_waves[peak_indices]
peak_dates = filtered_dates[peak_indices]

peaks_df = pd.DataFrame({'date': peak_dates, 'hs': peak_values})
peaks_df = peaks_df.sort_values('date')

storm_window = pd.Timedelta(days=34)
declustered_peaks = []

while not peaks_df.empty:
    # Get the highest peak in the current set
    max_idx = peaks_df['hs'].idxmax()
    max_row = peaks_df.loc[max_idx]
    declustered_peaks.append(max_row)

    # Remove all peaks within the storm window of this maximum
    mask = (peaks_df['date'] >= max_row['date'] - storm_window) & \
           (peaks_df['date'] <= max_row['date'] + storm_window)
    peaks_df = peaks_df[~mask]

# Convert back to arrays for your LSM/MLM math
declustered_df = pd.DataFrame(declustered_peaks).sort_values('date')
peak_values = declustered_df['hs'].values
peak_dates = declustered_df['date'].values

print(f"-----------------------\nSignificant wave heights:")
for i in range(len(peak_dates)):
    print(f"{peak_dates[i]} - {peak_values[i]} m")
print("-----------------------\n")

Hs = peak_values
Date = pd.to_datetime(peak_dates, format='%Y-%m-%d %H:%M:%S')

# LEAST SQUARE METHOD (LSM)

Hs = np.flip(np.sort(Hs)) # The waves are sorted by height
n = len(Hs) # Number of data points
i = np.arange(1, n+1) # Rank of each data point


F = 1 - i / (n + 1) # Weibull plotting position formula (Also used for Gumbel)

Y = -np.log(-np.log(F)) # Got new y for each data point

var = 1/n * np.sum((Y - np.mean(Y)) ** 2)
cov = 1/n * np.sum((Y - np.mean(Y)) * (Hs - np.mean(Hs)))

A_lsm = cov/var
B_lsm = np.mean(Hs) - A_lsm*np.mean(Y)

Hs_plot_lsm = A_lsm * Y + B_lsm
relative_error_lsm = (1/n) * np.sum(np.abs((Hs_plot_lsm - Hs) / Hs)) # E = (1/n) * Σ |(estimated - observed) / observed|

plt.figure()
plt.plot(Hs_plot_lsm, Y)
plt.plot(Hs, Y, "ro")
plt.xlabel("Significant wave height [m]")
plt.ylabel("Y")
# plt.title("LEAST SQUARE METHOD")
plt.show()

print(f"For Least Square Method\n-----------------------\nA: {A_lsm:.2f}, B: {B_lsm:.2f}")
print(f"Relative Error: {relative_error_lsm * 100:.2f}%\n")

# MAXIMUM LIKELIHOOD METHOD (MLM)

A_mlm, B_mlm, error_mlm = calculate_gumbel_parameters(Hs)

print(f"For Maximum Likelihood Method\n-----------------------------\nA: {A_mlm:.2f}, B: {B_mlm:.2f}")
print(f"Relative Error: {error_mlm * 100:.2f}%\n")

Hs_plot_mlm = A_mlm * Y + B_mlm

plt.figure()
plt.plot(Hs_plot_mlm, Y)
plt.plot(Hs, Y, "ro")
plt.xlabel("Significant wave height [m]")
plt.ylabel("Y")
# plt.title("MAXIMUM LIKELIHOOD METHOD")
plt.show()

# mu_mle, beta_mle = stats.gumbel_r.fit(annual_max)

# 6. CALCULATE 50-YEAR RETURN LEVEL
lamb = len(Hs) / ((Date.max() - Date.min()).days / 365.25)

T = 50 # Return period
F = 1 - 1 / (lamb * T)

Hs_50_MLM = A_mlm * (-np.log(-np.log(F))) + B_mlm
Hs_50_LSM = A_lsm * (-np.log(-np.log(F))) + B_lsm

print(f"Expected maximum wave height using MLM: {Hs_50_MLM:.2f} m")
print(f"Expected maximum wave height using LSM: {Hs_50_LSM:.2f} m")