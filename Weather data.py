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

airtemp=df.iloc[2:, 5].values
airtemp=airtemp.astype(float)
seatemp=df.iloc[2:, 12].values
seatemp=seatemp.astype(float)
DeltaT=airtemp-seatemp
DeltaT[DeltaT<-50]=np.nan #remove broken values
print(np.nanmin(DeltaT))
print(np.nanmax(DeltaT))

#assign values of R_T
R_T = []
for dt in DeltaT:
    if -15 <= dt < -12.5:
        R_T.append(1.21)
    elif -12.5 <= dt < -10:
        R_T.append(1.19)
    elif -10 <= dt < -7.5:
        R_T.append(1.19)
    elif -7.5 <= dt < -5:
        R_T.append(1.16)
    elif -5 <= dt < -2.5:
        R_T.append(1.13)
    elif -2.5 <= dt < -0:
        R_T.append(1)
    elif 0 <= dt < 2.5:
        R_T.append(0.92)
    elif 2.5 <= dt < 5:
        R_T.append(0.88)
    elif 5 <= dt < 7.5:
        R_T.append(0.84)
    elif 7.5 <= dt < 10:
        R_T.append(0.83)
    elif 10 <= dt < 12.5:
        R_T.append(0.81)
    elif 12.5 <= dt < 15:
        R_T.append(0.80)
    elif 15 <= dt < 17.5:
        R_T.append(0.79)
    elif 17.5 <= dt < 20:
        R_T.append(0.78)
    else:
        R_T.append(np.nan)
R_T = np.array(R_T) #Convert R_T back to numbers.

U_10=U_10*R_T
print(U_10)

