import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("vejrdata/Vejrdata 2018-2025.xlsx",sheet_name='Vejrdata 2018-2025')
windspeed = df.iloc[2:, 2].values
windspeed=windspeed.astype(float)
print(windspeed)

time=df.iloc[2:, 0].values
print(time)

z=15 #height of the measurement equipment of the wind
U_z=windspeed
U_10=U_z*(10/z)**(1/7)

print(U_10)

airtemp=df.iloc[4:, 1].values
airtemp=airtemp.astype(float)
seatemp=df.iloc[11:, 2].values
seatemp=seatemp.astype(float)
DeltaT=airtemp-seatemp
print(DeltaT)


