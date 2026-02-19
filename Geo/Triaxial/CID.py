import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

B = ["B8 805a","B14 1423a", "B8 881a", "B4 430a", "B8 829a"]
depth = ["22,0 - 22,5 m", "20,0 - 20,5 m", "25,0 - 25,6 m",  "32,0 - 32,6 m", "34,0 - 34,6 m"]

q_tp = np.array([766, 1141, 489, 881, 793 ])
sigma_3tp = np.array([848, 908, 1300, 1300, 1540 ])
sigma_1tp = np.array([1614, 2049, 1789, 2181, 2333])

q_p = np.array([766, 1141, 489, 881, 793])
sigma_3p = np.array([432, 468, 136, 313, 240 ])
sigma_1p = np.array([1198, 1609, 625, 1194, 1032])

q_cs = np.array([766, 1141, 461, 877, 775])
sigma_3cs = np.array([432, 468, 137, 314, 240 ])
sigma_1cs = np.array([1198, 1609, 598, 1194, 1015])

phi_tp = np.arcsin((sigma_1tp-sigma_3tp)/(sigma_1tp+sigma_3tp))
phi_tp = np.degrees(phi_tp)

phi_p = np.arcsin((sigma_1p-sigma_3p)/(sigma_1p+sigma_3p))
phi_p = np.degrees(phi_p)

phi_cs = np.arcsin((sigma_1cs-sigma_3cs)/(sigma_1cs+sigma_3cs))
phi_cs = np.degrees(phi_cs)

alpha_p = phi_p - phi_cs


df = pd.DataFrame()
df['Boreholes'] = B
df ['Depth' ] = depth
df['phi_tp'] = phi_tp
df['phi_p'] = phi_p
df['phi_cs'] = phi_cs
df['alpha_p'] = alpha_p


print("-"*100)
print(" "*45, "results"," "*45)
print("-"*100)
print(df)
print("-"*100)




