import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpmath import arange
from scipy.signal import find_peaks

########################################################################################
#Data and plot of raw data
df=pd.read_excel('1,96m 20min 290deg irregular.xlsx',header=None,skiprows=2)

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
plt.xlabel("Time (s)")
plt.ylabel("Surface height (m)")
plt.savefig('Raw data irregular')

################################################################################
#Zero down crossing

results = {}

for loc in locations:
    eta = Data[loc]['wave'].values
    t_målt = t

    # Find peaks (toppe) og troughs (dale)
    peaks, _ = find_peaks(eta, distance=5)
    troughs, _ = find_peaks(-eta, distance=5)

    wave_heights = []
    wave_periods = []
    wave_times = []

    i = 0  # index for troughs

    for j in range(len(peaks) - 1):
        start_peak = peaks[j]
        end_peak = peaks[j + 1]

        # find trough mellem to peaks
        trough_candidates = troughs[(troughs > start_peak) & (troughs < end_peak)]

        if len(trough_candidates) == 0:
            continue  # skip hvis ingen trough

        trough_idx = trough_candidates[np.argmin(eta[trough_candidates])]

        crest = eta[start_peak]
        trough = eta[trough_idx]

        H = crest - trough
        T = t_målt[end_peak] - t_målt[start_peak]

        wave_heights.append(H)
        wave_periods.append(T)
        wave_times.append(t_målt[start_peak])

    results[loc] = {
        'wave_heights': np.array(wave_heights),
        'wave_periods': np.array(wave_periods),
        'peak_times': np.array(wave_times)
    }


for loc in locations:
    plt.figure()
    plt.scatter(results[loc]['peak_times'], results[loc]['wave_heights'], s=10)
    plt.title(f"Peak-to-Peak bølgehøjder: {loc}")
    plt.xlabel("Tid (s)")
    plt.ylabel("Højde (m)")
    plt.gca().set_ylim(bottom=0)
    plt.xlabel('Time (s)')
    plt.ylabel('Wave height (m)')
    plt.savefig(f'Unfiltered wave heights at {loc}')

#Remove wave heights from before the simulation becomes steady.

idx={}
target=np.array([200,250,300,300,200,200,100,300])
for n in np.arange(len(target)):
    idx[locations[n]] = min(range(len(results[locations[n]]['peak_times'])), key=lambda i: abs(results[locations[n]]['peak_times'][i] - target[n]))

for loc in locations:
    i_cut = idx[loc]
    results[loc]['wave_heights'][:i_cut] = np.nan

for loc in locations:
    plt.figure()
    plt.scatter(results[loc]['peak_times'], results[loc]['wave_heights'])
    plt.title(f'Filtered wave heights at {loc}')
    plt.gca().set_ylim(bottom=0)
    plt.xlabel('Time (s)')
    plt.ylabel('Wave height (m)')
    plt.savefig(f'Filtered wave heights at {loc}')


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

coeff_real={}

realcoef=np.array([0.12,0.06,0.08,0.12,0.11,0.17,0.27,0.09])

for i in range(8):
    coeff_real[locations[i]]=realcoef[i]

deviation={}

for loc in locations:
    deviation[loc] = Disturbance_coefficients[loc] - coeff_real[loc]
    print(f'difference of disturbance coefficient at {loc} is {deviation[loc]:.2f}')

for i in range(8):
    print(f'Calculated at {locations[i]} is {Disturbance_coefficients[locations[i]]:.4f}, vs real {realcoef[i]:.4f}')