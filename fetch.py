import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# 4. Calculate effective fetches in P2 (Fetchs.xlsx and Fetchs.jpg) using
# Saville method (+/- 45 degrees);

df = pd.read_excel("ex1 data/fetchs.xlsx")
df = df.iloc[2:]
fetch = df['Unnamed: 2'].values
direction = df['Unnamed: 3'].values
direction = direction * np.pi / 180
direction = np.asarray(direction, dtype=float)

fetch = np.append(fetch, fetch[0])
direction = np.append(direction, direction[0])

plt.figure()
ax = plt.subplot(1, 1, 1, projection='polar')
ax.plot(direction, fetch)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
plt.title("Geographical Fetch")
plt.show()

direction = direction[1:]
eff_fetch = np.zeros(len(direction))

for i in range(len(direction)):

    idx = [(i + j) % len(direction) for j in range(-9, 9 + 1)] # Use index plus and minus 9 to weight the 45 deg angles.
    eff_fetch[i] = np.sum(fetch[idx] * np.cos(np.radians(direction[idx])) ** 2) / np.sum(np.cos(np.radians(direction[idx])))

eff_fetch = np.append(eff_fetch, eff_fetch[0])
direction = np.append(direction, direction[0])

plt.figure()
ax = plt.subplot(1, 1, 1, projection='polar')
ax.plot(direction, eff_fetch)
ax.set_theta_direction(-1)
ax.set_theta_offset(np.pi / 2.0)
plt.title("Effective Fetch")
plt.show()

df = pd.read_excel("ex1 data/U10.xlsx")
date = df['Unnamed: 0'].values
U10 = df['U10 (m/s)'].values

RT = 0.83 # Correction factor (Page 29 in literature)
U10_corrected = U10 * RT

U_A = 0.71 * U10_corrected**1.23

plt.figure()
plt.scatter(date,U_A)
plt.scatter(date,U10)
plt.xlabel("Date")
plt.ylabel("Velocity (m/s)")
plt.ylim([0, 25])
plt.legend(["UA", "U10"])
plt.show()

# 2. Calculate Hm0 and Tp using the SPM method at P2.
# ---------------------------------------------------

g = 9.82

# Index 38 is the 300 degrees direction
Hm0 = (0.0016 * (g * eff_fetch[38]*1000 / U_A**2)**0.5)*U_A**2/g
Tp = (0.2857 * (g * eff_fetch[38]*1000 / U_A**2)**(1/3))*U_A/g

print(f"Hm0 = {np.max(Hm0):.2f} m\nTp = {np.max(Tp):.2f} s")

plt.figure()
plt.scatter(date,Hm0)
plt.xlabel("Date")
plt.ylabel("Hm0 (m)")
plt.ylim([0, 8])
plt.legend(["SPM"])
plt.show()