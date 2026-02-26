import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
g = 9.82
B = ["B8 805a ","B14 1423a", "B8 881a ", "B4 430a ", "B8 829a "]
depth = ["22,0 - 22,5 m", "20,0 - 20,5 m", "25,0 - 25,6 m",  "32,0 - 32,6 m", "34,0 - 34,6 m"]
Test = ["CID","CIU","CID","CID","CID"]

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


tau_p = q_p/2
tau_cs = q_cs/2

e = np.array([0.418, 0.314, 0.561, 0.325, 0.309])

sigma_i = np.array([500, 536, 75, 150, 300])
rho_bulk = np.array([2.10, 2.26, 2.06, 2.25, 2.25])
gamma_sat = rho_bulk*g
gamma_w = 10
gamma_dry = gamma_sat - gamma_w

w = np.array([17.4, 9.9, 23.2, 12.2, 12.2 ])

sigma_pc = 800

OCR = sigma_pc/sigma_i

df = pd.DataFrame()
df['Boreholes'] = B
df ['Depth [m]' ] = depth
df['phi_tp [degree]'] = phi_tp
df['phi_p [degree]'] = phi_p
df['phi_cs [degree]'] = phi_cs
df['alpha_p [degree]'] = alpha_p

df1 = pd.DataFrame()
df1['Boreholes'] = B
df1 ['Depth [m]' ] = depth
df1['OCR [-]'] = OCR
df1['Void ratio [-]'] = e
df1['w [%]'] = w

df2 = pd.DataFrame()
df2['Gamma_sat [kN/m^2]'] = gamma_sat
df2['Gamma_dry [kN/m^2]'] = gamma_dry
df2['Type'] = Test




print("-"*100)
print(" "*45, "results"," "*45)
print("-"*100)
print(df)
print("-"*100)
print(df1)
print("-"*100)
print(df2)


