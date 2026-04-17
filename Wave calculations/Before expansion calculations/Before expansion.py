import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpmath import arange
from scipy.signal import find_peaks

########################################################################################
#Data and plot of raw data
df=pd.read_excel('20min 1,96m 290deg.xlsx',header=None,skiprows=2)

locations=['location 1','location 2','location 3','location 4','location 5','location 6','location 7','location 10']

Data={}
coloumns=[1,2,3,4,5,6,7,8]
for loc,col in zip(locations,coloumns):
    Data[loc]={'wave': df.iloc[:, col].astype(float)}

time_in_minutes=20
t = np.arange(0, time_in_minutes*60+0.5, 0.5)

plt.figure(1)
for loc in locations:
    plt.plot(t, Data[loc]['wave'],label=loc,linewidth=0.4)
plt.legend(fontsize='small')
plt.grid(True)

################################################################################
#Zero down crossing

results = {}

for loc in locations:
    eta = Data[loc]['wave'].values
    t_målt = t
    peaks, _ = find_peaks(eta, distance=5)

    wave_heights = []
    wave_periods = []
    peak_times = t_målt[peaks]

    for j in range(len(peaks) - 1):

        start_idx = peaks[j]
        end_idx = peaks[j + 1]

        wave_segment = eta[start_idx:end_idx]

        H = eta[start_idx] - wave_segment.min()

        T = t_målt[end_idx] - t_målt[start_idx]

        wave_heights.append(H)
        wave_periods.append(T)

    results[loc] = {
        'wave_heights': np.array(wave_heights),
        'wave_periods': np.array(wave_periods),
        'peak_times': peak_times[:-1]
    }


for loc in locations:
    plt.figure()
    plt.scatter(results[loc]['peak_times'], results[loc]['wave_heights'], s=10)
    plt.title(f"Peak-to-Peak bølgehøjder: {loc}")
    plt.xlabel("Tid (s)")
    plt.ylabel("Højde (m)")

#Remove wave heights from before the simulation becomes steady.

idx={}
target=np.array([400,400,600,380,225,200,200,250])
for n in np.arange(len(target)):
    idx[locations[n]] = min(range(len(results[locations[n]]['peak_times'])), key=lambda i: abs(results[locations[n]]['peak_times'][i] - target[n]))

for loc in locations:
    i_cut = idx[loc]
    results[loc]['wave_heights'][:i_cut] = np.nan

for loc in locations:
    plt.figure()
    plt.scatter(results[loc]['peak_times'], results[loc]['wave_heights'])
    plt.title(f'Filtered wave heights at {loc}')


#########################################################################################################
#Disturbance coefficients
H_i=1.96 #Incident wave in model

means={}
for loc in locations:
    means[loc]=np.nanmean(results[loc]['wave_heights'])

Disturbance_coefficients={}
for loc in locations:
    Disturbance_coefficients[loc]=means[loc]/H_i

for loc in locations:
    print(f'Disturbance coefficients for {loc} = {Disturbance_coefficients[loc]:.2f}')

plt.show()


