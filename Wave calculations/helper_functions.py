import math
import numpy as np
from scipy.optimize import fsolve

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