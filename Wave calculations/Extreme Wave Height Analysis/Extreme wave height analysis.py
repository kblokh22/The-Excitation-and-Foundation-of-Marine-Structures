import pandas as pd
import numpy as np
from scipy import stats
import openpyxl as pyx
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import alpha

#                                                   Define Wave Values

# Local path to file:
file_path = r"C:\Users\lukac\Desktop\Materials\2 Semestar\Projekt\Python\Extreme wave height data\Vejrdata 2018-2025.xlsx"

try:
    # 2. Load the Excel file, skipping the first row if it contains extra header info.

    df = pd.read_excel(file_path, skiprows=1)

    # 3. Convert the timestamp column to datetime, coerce errors to NaT.
    df['Tidspunkt'] = pd.to_datetime(df['Tidspunkt'], dayfirst=True, errors='coerce')

    # 4. Remove rows where either the timestamp or wave height is missing.
    df = df.dropna(subset=['Tidspunkt', 'Mid. bølg [m]'])

    # 5. Extract the year from the timestamp.
    df['Year'] = df['Tidspunkt'].dt.year

    # 6. Compute the annual maximum significant wave height.
    annual_max = df.groupby('Year')['Mid. bølg [m]'].max()

    # 7. Display the result.
    print("Annual maximum significant wave height [m]:")
    print(annual_max)

except FileNotFoundError:
    print("Error: File not found. Please check the file path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

print ("------------------------------------------------------")

# Significant Wave Height
Hs = np.array([2.41, 2.92, 3.17, 3.35, 3.65, 3.78, 3.81, 3.83])
Hs = np.sort(Hs)
N = len(Hs)
#-----------------------------------------------------------------------------------------------------------------------

#                                                 Gumbel Probability


                                                # LEAST SQUARE METHOD

print("Least Square estimates:")

x = np.sort(Hs)          # wave heights in ascending order
n = len(x)
alpha = 0.3               # plotting position parameter (Benard)

# Correct plotting positions (non-exceedance)
i = np.arange(1, n + 1)
F = (i - alpha) / (n + 1 - 2 * alpha)

# Reduced Gumbel variate
Y = -np.log(-np.log(F))

# Linear regression: x = A * Y + B
coefficients = np.polyfit(Y, x, deg=1)   # x = A*Y + B
A, B = coefficients

print("A =", A)
print("B =", B)
print("We will use these values as estimations for the Maximum Likelihood Method")
print ("------------------------------------------------------")


                                              # MAXIMUM LIKELIHOOD METHOD

def neg_log_likelihood_gumbel(params):
    A, B = params
    if A <= 0:  # scale must be positive
        return 1e10
    # Avoid numerical overflow when (x - B) is too large positive
    # (Gumbel is defined for all real x, but exp(-exp(...)) can explode)
    # We clip the argument of the inner exp to a reasonable range.
    term1 = n * np.log(A)
    term2 = np.sum((Hs - B) / A)
    # term3 = sum(exp(-(x-B)/A)); use np.exp with caution
    arg = -(Hs - B) / A
    # Clip arg to avoid overflow in exp (exp(>700) is huge)
    arg_clipped = np.clip(arg, -700, 700)
    term3 = np.sum(np.exp(arg_clipped))
    return term1 + term2 + term3


# Initial guess from LSM
initial_guess = [A, B]

# Optimisation
result = minimize(neg_log_likelihood_gumbel,
                  initial_guess,
                  method='Nelder-Mead')  # or 'BFGS'

A_mlm, B_mlm = result.x

print("Maximum Likelihood estimates:")
print(f"A_mlm = {A_mlm:.4f}")
print(f"B_mlm = {B_mlm:.4f}")

# ----------------------------------------------------------------------------------------------------------------------
                                                        # PLOT

x_plot = np.linspace(x.min(), x.max(), 100)
Y_lsm = (x_plot - B) / A          # line corresponding to LSM parameters
Y_mlm = (x_plot - B_mlm) / A_mlm  # line for MLM parameters

plt.figure(figsize=(8, 5))
plt.plot(x, Y, 'o', label='Observed data')                     # points
plt.plot(x_plot, Y_lsm, '--', label=f'LSM fit: A={A:.3f}, B={B:.3f}')
plt.plot(x_plot, Y_mlm, '-', label=f'MLM fit: A={A_mlm:.3f}, B={B_mlm:.3f}')
plt.xlabel('Wave height (m)')
plt.ylabel('Reduced variate Y = -ln(-ln(F))')
plt.title('Gumbel probability plot')
plt.legend()
plt.grid(True)
plt.show()

print ("------------------------------------------------------")

#                                                   Design Wave Height

T_design = 50
lamb = 1         # lamb = no. of extreme data / no. of years observed

# Value of the design wave height (x_T):
x_design = A_mlm * (-np.log(-np.log(1 - 1/(lamb * T_design)))) + B_mlm
print("Design wave height:", x_design)
print ("------------------------------------------------------")

#                                                   Encounter Probability

L= 50  #Lifetime
p = 1- (1-(1/T_design))**L
print("Encounter Probability", p)
print("Probability for the design situation is exceeded within the lifetime of the structure (%):", p*100)
print ("------------------------------------------------------")