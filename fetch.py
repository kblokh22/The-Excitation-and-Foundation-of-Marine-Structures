import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("Weather data/fetch_results.csv")
direction = df['bearing_deg'].values # Given in degrees in 3 deg intervals
length = df['length_km'].values # Given in km

direction = direction * np.pi / 180 # Converting to radians
direction = np.asarray(direction, dtype=float)

length = np.append(length, length[0])
direction = np.append(direction, direction[0])

# Geographical Fetch
plt.figure()
ax = plt.subplot(1, 1, 1, projection='polar')
ax.plot(direction, length)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
plt.title("Geographical Fetch")
plt.show()

direction = direction[1:]
eff_fetch = np.zeros(len(direction))

for i in range(len(direction)):

    idx = [(i + j) % len(direction) for j in range(-15, 15 + 1)] # Use index plus and minus 15 to weight the 45 deg angles.
    eff_fetch[i] = np.sum(length[idx] * np.cos(np.radians(direction[idx])) ** 2) / np.sum(np.cos(np.radians(direction[idx])))

eff_fetch = np.append(eff_fetch, eff_fetch[0])
direction = np.append(direction, direction[0])

# Effective Fetch
plt.figure()
ax = plt.subplot(1, 1, 1, projection='polar')
ax.plot(direction, eff_fetch)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
plt.title("Effective Fetch")
plt.show()

direction = direction[1:]
SPM_fetch = np.zeros(len(direction))

for i in range(len(direction)):

    idx = [(i + j) % len(direction) for j in range(-4, 4 + 1)] # Use index plus and minus 4 to get a total of 9 angles.
    SPM_fetch[i] = np.sum(length[idx]) / 9
    print(idx, SPM_fetch[i])

SPM_fetch = np.append(SPM_fetch, SPM_fetch[0])
direction = np.append(direction, direction[0])

# SPM Fetch
plt.figure()
ax = plt.subplot(1, 1, 1, projection='polar')
ax.plot(direction, SPM_fetch)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
plt.title("SPM Fetch")
plt.show()


print(f'Effective Fetch: \x1b[92m{np.max(eff_fetch)}\x1b[0m')
print(f'SPM Fetch: \x1b[94m{np.max(SPM_fetch)}\x1b[0m')