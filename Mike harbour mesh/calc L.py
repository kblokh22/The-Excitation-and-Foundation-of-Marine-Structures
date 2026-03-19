import numpy as np

def waveLengthIteration(wave_period, water_depth):
    """
    Returns
    -------
    L : Final wavelength
    n : Number of iterations performed
    """
    gravity = 9.81

    # Initial guess (deep water wave)
    L = [(gravity * wave_period ** 2) / (2 * np.pi)]
    n = 1

    while True:
        L_next = ((gravity * wave_period ** 2) / (2 * np.pi)) * np.tanh((2 * np.pi * water_depth) / L[n - 1])
        L.append(L_next)

        # Convergence check
        if abs(L[n-1] / L[n] - 1) < 1e-5:
            break

        n += 1

        if n > 1000:
            print("waveLengthIteration did not converge!")
            break

    print(f"Wave length found to be {L[-1]:.2f} m after {n} iterations.")
    return L[-1]


L=waveLengthIteration(8,4)
x=4/L

print(x)