import numpy as np
import pandas as pd
from fetch import SPM_fetch


df = pd.read_excel("Weather data/Vejrdata 2018-2025.xlsx",sheet_name='Vejrdata 2018-2025')
windspeed = df.iloc[2:, 2].values
windspeed=windspeed.astype(float)

time=df.iloc[2:, 0].values


U_z=windspeed
''' Assumed collected at 10m
z=15 #height of the measurement equipment of the wind
U_10=U_z*(10/z)**(1/7)
'''
U_10=U_z
airtemp=df.iloc[2:, 5].values
airtemp=airtemp.astype(float)
seatemp=df.iloc[2:, 12].values
seatemp=seatemp.astype(float)
h=df.iloc[2:, 1].values
h=h.astype(float)
swl=7 #mean water level reference
h=h+swl

DeltaT=airtemp-seatemp
DeltaT[DeltaT<-50]=np.nan #remove broken values
print(f'The minimum air-sea temp difference is {np.nanmin(DeltaT)} C')
print(f'The maximum air-sea temp difference is {np.nanmax(DeltaT)} C')

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

#Correct U10 for RT.
U_10=U_10*R_T

#Calculate UA
U_A=0.71*U_10**1.23

#Maximize fetch
SPM_fetch=max(SPM_fetch)*1000
print(f'The maximum fetch is {SPM_fetch} m')

g=9.82

#avoid dividing by nan ind calculation of hm0 and Tp
valid = (~np.isnan(U_A)) & (U_A != 0) & (~np.isnan(h)) & (h > 0)

Hm0 = np.full_like(U_A, np.nan)
Tp  = np.full_like(U_A, np.nan)
#U_A[valid]

Hm0[valid] = (0.283*np.tanh( 0.53 * ( (g*h[valid])/(U_A[valid]**2) )**(3/4) )
              *np.tanh( (0.00565* ( g*SPM_fetch/(U_A[valid]**2) )**(1/2))/( np.tanh( 0.53*(g*h[valid]/(U_A[valid]**2))**(3/4) ) ) )
              *(U_A[valid]**2 /g))
print(f'The significant wave height is calculated as {Hm0}\n and the maximum value of HM0 is {np.max(Hm0[valid])}')

Tp[valid] = (7.54*np.tanh( 0.833 * (g*h[valid]/U_A[valid]**2)**(3/8) )
             *np.tanh((0.0379*(g*SPM_fetch/(U_A[valid]**2))**(1/3))/( np.tanh( 0.833*(g*h[valid]/(U_A[valid]**2))**(3/8) ) ))    )

Hm0max=np.max(Hm0[valid])
indices = np.where(Hm0 == Hm0max)[0]
print("Maximum value of Hm0 occurs at array number:", indices)

Tp_to_Hm0max=Tp[indices]
print("The matching Tp for max value of Hm0 is",Tp_to_Hm0max)