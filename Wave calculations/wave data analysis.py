import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy.ndimage import label, maximum_position
from scipy.stats import weibull_min

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

mid_waves = np.where(max_waves > 8, np.nan, mid_waves)

# Filter out NaN values in max waves
mask = ~np.isnan(mid_waves)
filtered_dates = dates[mask]
filtered_waves = mid_waves[mask]

# Find peaks in filtered waves
mask = filtered_waves > 3.8
labels, num_features = label(mask)
peak_indices = maximum_position(filtered_waves, labels, range(1, num_features + 1))

# Extract peak values
peak_indices = [idx[0] for idx in peak_indices]
peak_values = filtered_waves[peak_indices]
peak_dates = filtered_dates[peak_indices]

peak_values = np.delete(peak_values, [1, 2, 4])
peak_dates = np.delete(peak_dates, [1, 2, 4])

plt.figure()
plt.plot(filtered_dates, filtered_waves)
plt.plot(peak_dates, peak_values, 'ro')
plt.xlabel('Date')
plt.ylabel('Significant wave height [m]')
plt.title('Water level over time')
plt.show()

print(f"-----------------------\nSignificant wave heights:")
for i in range(len(peak_dates)):
    print(f"{peak_dates[i]} - {peak_values[i]} m")
print("-----------------------\n")

Hs = peak_values
Date = pd.to_datetime(peak_dates, format='%Y-%m-%d %H:%M:%S')

# LEAST SQUARE METHOD (LSM)

k = np.linspace(1, 4, 500)
Y, A, B, Hs_plot, relative_error = [], [], [], [], []

for idx, k_lsm in enumerate(k):

    Hs = np.flip(np.sort(Hs)) # The waves are sorted by height
    n = len(Hs) # Number of data points
    i = np.arange(1, n+1) # Rank of each data point


    F = 1 - i / (n + 1) # Weibull plotting position formula

    Y_lsm = (-np.log(1 - F))**(1/k_lsm) # Got new y for each data point

    var = 1/n * np.sum((Y_lsm - np.mean(Y_lsm))**2)
    cov = 1/n * np.sum((Y_lsm - np.mean(Y_lsm))*(Hs - np.mean(Hs)))

    A_lsm = cov/var
    B_lsm = np.mean(Hs) - A_lsm*np.mean(Y_lsm)

    Hs_plot_lsm = A_lsm*Y_lsm + B_lsm
    relative_error_lsm = (1/n) * np.sum(np.abs((Hs_plot_lsm - Hs) / Hs)) # E = (1/n) * Σ |(estimated - observed) / observed|

    Y.append(Y_lsm)
    A.append(A_lsm)
    B.append(B_lsm)
    Hs_plot.append(Hs_plot_lsm)
    relative_error.append(relative_error_lsm)

A = A[relative_error.index(min(relative_error))]
B = B[relative_error.index(min(relative_error))]
Y = Y[relative_error.index(min(relative_error))]
k_lsm = k[relative_error.index(min(relative_error))]
Hs_plot = Hs_plot[relative_error.index(min(relative_error))]
relative_error = relative_error[relative_error.index(min(relative_error))]

plt.figure()
plt.plot(Hs_plot, Y)
plt.plot(Hs, Y, "ro")
plt.xlabel("x")
plt.ylabel("y")
plt.title("LEAST SQUARE METHOD")
plt.show()

print(f"For Least Square Method\n-----------------------\nA: {A:.2f}, B: {B:.2f}")
print(f"Relative Error: {relative_error * 100:.2f}%\n")

# MAXIMUM LIKELIHOOD METHOD (MLM)

k_mlm, B_mlm, A_mlm = weibull_min.fit(Hs)

Y = (-np.log(1 - F))**(1/k_mlm)

Hs_plot = A_mlm * Y + B_mlm

n = len(Hs)
error_mlm = (1 / n) * np.sum(np.abs((Hs_plot - Hs) / Hs))

plt.figure()
plt.plot(Hs_plot, Y)
plt.plot(Hs, Y, "ro")
plt.xlabel("x")
plt.ylabel("y")
plt.title("MAXIMUM LIKELIHOOD METHOD")
plt.show()

print(f"For Maximum Likelihood Method\n-----------------------------\nA: {A_mlm:.2f}, B: {B_mlm:.2f}, k: {k_mlm:.2f}")
print(f"Relative Error: {error_mlm:.2f}%\n")

# Calculate Hs,50 and the expected maximum wave height

# Define the sample intensity (number of extreme data / number of years of observation)

lamb = len(Hs) / ((Date.max() - Date.min()).days / 365.25)

T = 50 # Return period
F = 1 - 1 / (lamb * T)

Hs_50 = A_mlm * (-np.log(1 - F))**(1/k_mlm) + B_mlm
Hs_50_LSM = A * (-np.log(1 - F))**(1/k_lsm) + B

print(f"Expected maximum wave height using MLM: {Hs_50:.2f} m")
print(f"Expected maximum wave height using LSM: {Hs_50_LSM:.2f} m")