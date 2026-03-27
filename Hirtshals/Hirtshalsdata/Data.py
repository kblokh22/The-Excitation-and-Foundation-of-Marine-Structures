import pandas as pd
import inspect
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt

#Load data
def csv_to_vars(Names, DirectoryAndName, Coloumns, FirstRow):
    df = pd.read_csv(DirectoryAndName, header=None)
    caller_globals = inspect.currentframe().f_back.f_globals

    for i in range(len(Names)):
        caller_globals[Names[i]] = df.iloc[FirstRow:, Coloumns[i]].to_numpy(dtype=float, copy=True)



def excel(Names,DirectoryAndName,SheetName,Coloumns,FirstRow):
    #Names is an array of strings that will be returned as the name of the coloumns
    #DirectoryAndName is a string containing the directory and name of the excel document
    #Sheetname is a string of the sheet name
    #FirstRow is the first row of every coloumn (where to start counting)
    df = pd.read_excel(DirectoryAndName,sheet_name=SheetName,header=None)
    caller_globals = inspect.currentframe().f_back.f_globals
    for i in range(len(Names)):
        caller_globals[Names[i]] = df.iloc[FirstRow:, Coloumns[i]].values


Names=np.array([['t1','dist1','time1'],['t2','dist2','time2'],['t3','dist3','time3'],['t4','dist4','time4'],['t5','dist5','time5'],['t6','dist6','time6'],['t7','dist7','time7'],['t10','dist10','time10']])
DirectoryAndName=np.array([['ultrasonic_data_1_20260326_100946.csv'],['ultrasonic_data_2_20260326_103145.csv'],['ultrasonic_data_3_20260326_093946.csv'],['ultrasonic_data_4_20260326_081840.csv'],['ultrasonic_data_5_20260326_075141.csv'],['ultrasonic_data_6_20260326_090830.csv'],['ultrasonic_data_7_20260326_084910.csv'],['ultrasonic_data_10_20260326_104932.csv']])
Coloumns=np.array([0,1,2])
FirstRow=0

for i in range(len(Names)):
    csv_to_vars(Names[:][i], DirectoryAndName[i][0], Coloumns, FirstRow)
########################################################################################

#Remove invalid data points and move mean to 0:
dist=[dist1,dist2,dist3,dist4,dist5,dist6,dist7,dist10]
for d in dist:
    d[d <= 0] = np.nan
    d[d > np.nanmean(d)*1.5] = np.nan
    d[d < np.nanmean(d) * (-1.5)] = np.nan


for d in dist:
    d-=np.nanmean(d)
########################################################################################

#Convert the time array from unix to real time
for i in range(len(Names)):
    time_array = globals()[Names[i][2]]
    converted = [
        datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        for ts in time_array
    ]
    globals()[Names[i][2]] = np.array(converted)

time = [time1, time2, time3, time4, time5, time6, time7, time10]
########################################################################################

#Plot
location=['Location 1', 'Location 2', 'Location 3', 'Location 4', 'Location 5', 'Location 6', 'Location 7', 'Location 10']

for i in range(len(Names)):
    plt.figure(i)
    t = globals()[Names[i][0]]
    t = t - t[0]
    dist = globals()[Names[i][1]]
    plt.plot(t,dist)
    plt.title(f'{location[i]}, {time[i][0]} to {time[i][-1]}')



########################################################################################

#Zero down crossing analysis
# 2. Using the down-crossing method to calculate H_max,
# T_Hmax, H_1/250, T_1/250, H_1/100, H_1/3, T_H1/3, H_mean,
# T_mean, H_rms of signal.mat;

eta = signal - np.mean(signal)
crossings = np.where((eta[:-1] > 0) & (eta[1:] <= 0))[0]

wave_heights = []
wave_periods = []

for i in range(len(crossings) - 1):
    start = crossings[i]
    end = crossings[i + 1]

    wave = eta[start:end]
    H = wave.max() - wave.min()
    T = (end - start) / fs

    wave_heights.append(H)
    wave_periods.append(T)

wave_heights = np.array(wave_heights)
wave_periods = np.array(wave_periods)

wave_heights_sorted = np.sort(wave_heights)
wave_periods_sorted = wave_periods[np.argsort(wave_heights)]

H_max = wave_heights.max()
T_Hmax = wave_periods[wave_heights.argmax()]

H_1_250 = wave_heights_sorted[-floor(len(wave_heights_sorted)/250):].mean()
T_1_250 = wave_periods_sorted[-floor(len(wave_periods_sorted)/250):].mean()

H_1_100 = wave_heights_sorted[-floor(len(wave_heights_sorted)/100):].mean()

H_1_3 = wave_heights_sorted[-floor(len(wave_heights_sorted)/3):].mean()
T_H1_3 = wave_periods_sorted[-floor(len(wave_periods_sorted)/3):].mean()

H_mean = np.mean(wave_heights)
T_mean = np.mean(wave_periods)

H_rms = np.sqrt(np.mean(np.square(wave_heights)))

#Keep show in bottom
plt.show()