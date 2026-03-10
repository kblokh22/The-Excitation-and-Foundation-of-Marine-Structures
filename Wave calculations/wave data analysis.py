from matplotlib import pyplot as plt
from helper_functions import *

peak_dates, peak_values, filtered_dates, filtered_waves = load_wave_data("Weather data/Samlet vejrdata 2013.2019-NK.xlsx", "Weather data/Vejrdata 2018-2025.xlsx")

plt.figure()
plt.plot(filtered_dates, filtered_waves)
plt.plot(peak_dates, peak_values, 'ro')
plt.xlabel('Date')
plt.ylabel('Significant wave height [m]')
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


    F = 1 - ((i - 0.3) / (n + 0.4)) # Weibull plotting position formula

    Y_lsm = (-np.log(1 - F))**(1/k_lsm) # Got new y for each data point

    var = 1/n * np.sum((Y_lsm - np.mean(Y_lsm))**2)
    cov = 1/n * np.sum((Y_lsm - np.mean(Y_lsm))*(Hs - np.mean(Hs)))

    A_lsm = cov/var
    B_lsm = np.mean(Hs) - A_lsm*np.mean(Y_lsm)

    Hs_plot_lsm = A_lsm*Y_lsm + B_lsm
    relative_error_lsm = (1/n) * (np.sum(np.abs((Hs_plot_lsm - Hs) / Hs))) # E = (1/n) * Σ |(estimated - observed) / observed|

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
plt.xlabel("Significant wave height [m]")
plt.ylabel("Y")
# plt.title("LEAST SQUARE METHOD")
plt.show()

print(f"For Least Square Method\n-----------------------\nA: {A:.2f}, B: {B:.2f}")
print(f"Relative Error: {relative_error * 100:.2f}%\n")

# MAXIMUM LIKELIHOOD METHOD (MLM)

B_mlm, k_mlm, A_mlm, error_mlm = find_best_B(Hs)

Y = (-np.log(1 - F))**(1/k_mlm)

Hs_plot = A_mlm * Y + B_mlm

relative_error_mlm = (1/n) * (np.sum(np.abs((Hs_plot - Hs) / Hs)))

plt.figure()
plt.plot(Hs_plot, Y)
plt.plot(Hs, Y, "ro")
plt.xlabel("Significant wave height [m]")
plt.ylabel("Y")
# plt.title("MAXIMUM LIKELIHOOD METHOD")
plt.show()

print(f"For Maximum Likelihood Method\n-----------------------------\nA: {A_mlm:.2f}, B: {B_mlm:.2f}, k: {k_mlm:.2f}")
print(f"Relative Error: {relative_error_mlm * 100:.2f}%\n")

# Calculate Hs,50 and the expected maximum wave height

# Define the sample intensity (number of extreme data / number of years of observation)

lamb = len(Hs) / ((Date.max() - Date.min()).days / 365.25)

T = 50 # Return period
F = 1 - 1 / (lamb * T)

Hs_50 = A_mlm * (-np.log(1 - F))**(1/k_mlm) + B_mlm
Hs_50_LSM = A * (-np.log(1 - F))**(1/k_lsm) + B

print(f"Expected maximum wave height using MLM: {Hs_50:.2f} m")
print(f"Expected maximum wave height using LSM: {Hs_50_LSM:.2f} m")