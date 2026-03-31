import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# the values are found by looking at the graphs

B = ["B4","B5", "B8", "B11"]
depth = ["26,0 - 26,3 m", "16,0 - 16,7 m", "22,0 - 22,5 m",  "16,0 - 16,6 m"]

q = np.array([190, 480, 420, 600])
varep = np.array([0.15, 0.15, 0.05, 0.15,])
w = np.array([15.89, 20.67, 16.98, 16.23])


c_u = q/2
df = pd.DataFrame()
df["Boreholes"] = B
df["depth [m]"] = depth
df["q [kPa]"] = q
df["varep [%]"] = varep
df["c_u [kPa]"] = c_u
df["w [%]"] = w

print("-"*100)
print(" "*45, "results"," "*45)
print("-"*100)
print(df.round(2))
print("-"*100)

val = df["c_u [kPa]"].iloc[1:].mean() - 1.645*df["c_u [kPa]"].iloc[1:].std()
print(val)
c_d = val/1.8
print(c_d)
print("-"*100)
