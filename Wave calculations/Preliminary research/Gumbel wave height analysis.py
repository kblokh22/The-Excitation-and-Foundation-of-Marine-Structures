import matplotlib.pyplot as plt
from helper_functions import *

peak_dates, peak_values, filtered_dates, filtered_waves = load_wave_data("Weather data/Samlet vejrdata 2013.2019-NK.xlsx", "Weather data/Vejrdata 2018-2025.xlsx")

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