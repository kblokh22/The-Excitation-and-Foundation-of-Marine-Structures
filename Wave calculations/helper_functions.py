import math
import numpy as np
from scipy.optimize import fsolve
import pandas as pd
from scipy.ndimage import label, maximum_position

def load_wave_data(filepath1, filepath2):
    years = np.arange(2013, 2019)

    dates = []
    water_levels = []
    mid_waves = []
    max_waves = []

    for year in years:
        df = pd.read_excel(filepath1, sheet_name=f'{year}')

        dates.extend(df['Tidspunkt'].iloc[1:])
        water_levels.extend(df['Vandstand [m]'].iloc[1:])
        mid_waves.extend(df['Mid. bølg [m]'].iloc[1:])
        max_waves.extend(df['Max. bølg. [m]'].iloc[1:])

    df = pd.read_excel(filepath2)

    date = pd.to_datetime(df['Column1'].iloc[2:].values, format='%d/%m/%Y %H:%M:%S')
    water_level = df['Column2'].iloc[2:].astype(float)
    mid_wave = df['Column7'].iloc[2:].astype(float)
    max_wave = df['Column8'].iloc[2:].astype(float)

    dates.extend(date)
    water_levels.extend(water_level)
    mid_waves.extend(mid_wave)
    max_waves.extend(max_wave)

    dates = np.array(dates)
    mid_waves = np.array(mid_waves)

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

    # 1. Create a DataFrame for easier time manipulation
    peaks_df = pd.DataFrame({'date': peak_dates, 'hs': peak_values})
    peaks_df = peaks_df.sort_values('date')

    # 2. Define the storm window (e.g., 2 days)
    storm_window = pd.Timedelta(days=34)

    # 3. De-clustering Algorithm
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

    # 4. Convert back to arrays for your LSM/MLM math
    declustered_df = pd.DataFrame(declustered_peaks).sort_values('date')
    peak_values = declustered_df['hs'].values
    peak_dates = declustered_df['date'].values

    return peak_dates, peak_values, filtered_dates, filtered_waves

def calculate_mle_k_a(data, x_prime, tol=1e-6):
    """Newton-Raphson to find k and A for a specific B (x_prime)."""
    N = len(data)
    y = [x - x_prime for x in data]
    sum_ln_y = sum(math.log(val) for val in y)

    k = 1.0  # Initial guess for k
    for _ in range(100):
        s0 = sum(val ** k for val in y)
        s1 = sum(val ** k * math.log(val) for val in y)
        s2 = sum(val ** k * (math.log(val) ** 2) for val in y)

        f_k = N + k * sum_ln_y - (N * k * s1 / s0)
        # Analytical derivative f'(k)
        df_k = sum_ln_y - N * ((s1 / s0) + k * (s0 * s2 - s1 ** 2) / (s0 ** 2))

        k_new = k - f_k / df_k
        if abs(k_new - k) < tol:
            k = k_new
            break
        k = k_new

    A = ((1.0 / N) * sum(val ** k for val in y)) ** (1.0 / k)
    return k, A


def find_best_B(data, start_B=3.0, step=0.01):
    """Loops through values of B to find the one that minimizes Mean Error."""
    N = len(data)
    sorted_data = sorted(data)
    # B must be smaller than the minimum x in the dataset
    limit_B = sorted_data[0] - 0.01

    best_B = start_B
    min_error = float('inf')
    best_k = 0
    best_A = 0

    current_B = start_B
    while current_B < limit_B:
        try:
            k, A = calculate_mle_k_a(data, current_B)

            # Goodness of Fit: Mean Error (E)
            # Calculated by comparing empirical CDF to the Weibull CDF
            # Weibull CDF: F(x) = 1 - exp(-((x - B)/A)^k)
            total_error = 0
            for i, x in enumerate(sorted_data):
                empirical_cdf = (i + 1) / (N + 1)
                theoretical_cdf = 1 - math.exp(-((x - current_B) / A) ** k)
                total_error += abs(empirical_cdf - theoretical_cdf)

            mean_error = (total_error / N) * 100

            if mean_error < min_error:
                min_error = mean_error
                best_B = current_B
                best_k = k
                best_A = A
        except:
            pass  # Skip values where Newton-Raphson fails to converge

        current_B += step

    return best_B, best_k, best_A, min_error

def calculate_gumbel_parameters(data):
    x = np.array(data)
    N = len(x)
    mean_x = np.mean(x)

    # Solve for A using iteration (Newton-Raphson)
    # Equation: sum(xi * exp(-xi/A)) - (mean(x) - A) * sum(exp(-xi/A)) = 0
    def equation_for_A(A):
        term1 = np.sum(x * np.exp(-x / A))
        term2 = (mean_x - A) * np.sum(np.exp(-x / A))
        return term1 - term2

    # Initial guess for A (standard deviation related)
    initial_guess = np.std(x) * np.sqrt(6) / np.pi
    A_fit = fsolve(equation_for_A, initial_guess)[0]

    # Calculate B
    # Equation: B = A * ln[N / sum(exp(-xi/A))]
    sum_exp = np.sum(np.exp(-x / A_fit))
    B_fit = A_fit * np.log(N / sum_exp)

    # Calculate Average Relative Error E
    x_observed = np.sort(x)
    p = (np.arange(1, N + 1) - 0.44) / (N + 0.12)  # Standard plotting position
    x_estimated = B_fit - A_fit * np.log(-np.log(p))

    relative_errors = np.abs(x_estimated - x_observed) / x_observed
    avg_relative_error = np.mean(relative_errors)

    return A_fit, B_fit, avg_relative_error