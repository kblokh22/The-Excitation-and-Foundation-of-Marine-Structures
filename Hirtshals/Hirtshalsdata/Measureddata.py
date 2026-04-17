import pandas as pd
import inspect
import numpy as np
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import matplotlib.pyplot as plt
from math import floor
from scipy.fft import fft, fftfreq

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
dist1_unfiltered=dist1.copy()
dist2_unfiltered=dist2.copy()
dist3_unfiltered=dist3.copy()
dist4_unfiltered=dist4.copy()
dist5_unfiltered=dist5.copy()
dist6_unfiltered=dist6.copy()
dist7_unfiltered=dist7.copy()
dist10_unfiltered=dist10.copy()
dist_unfiltered=[dist1_unfiltered,dist2_unfiltered,dist3_unfiltered,dist4_unfiltered,dist5_unfiltered,dist6_unfiltered,dist7_unfiltered,dist10_unfiltered]


########################################################################################
# Filtering data
val=1.5 #was 1.5
for d in dist:
    d[d <= 0] = np.nan
    d[d > np.nanmean(d)*val] = np.nan
    d[d < np.nanmean(d) * (-val)] = np.nan
# Putting the mean at 0 (MWL)
for d,du in zip(dist,dist_unfiltered):
    thatthing = np.nanmean(d)
    d-=np.nanmean(d)
    du-=thatthing # use d not du cause unfiltered data will skew from filtered data

#Convert dist from [mm] to [m]
for d,du in zip(dist,dist_unfiltered):
    d/=1000
    du/=1000


#Convert the time array from unix to real time
tz = ZoneInfo("Europe/Copenhagen")
offset_sekunder = 3600

for i in range(len(Names)):
    time_array = globals()[Names[i][2]]
    time_array_corrected = time_array - offset_sekunder

    converted = [
        datetime.fromtimestamp(ts, tz)
        .strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        for ts in time_array_corrected
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
    plt.xlabel('Time [s]')
    plt.ylabel('Distance [m]')
    plt.plot(t,dist)
    plt.title(f'{location[i]}, {time[i][0]} to {time[i][-1]}')
    plt.savefig(f'{location[i]} raw data.png')



########################################################################################

#Zero down crossing analysis

results = {}

for i in range(len(Names)):
    eta = globals()[Names[i][1]]
    t_målt = globals()[Names[i][0]]

    mask = ~np.isnan(eta)
    eta = eta[mask]
    t_målt = t_målt[mask]

    crossings = np.where((eta[:-1] > 0) & (eta[1:] <= 0))[0]

    wave_heights = []
    wave_periods = []

    for j in range(len(crossings) - 1):
        start = crossings[j]
        end = crossings[j + 1]

        wave = eta[start:end]
        H = wave.max() - wave.min()

        T = t_målt[end] - t_målt[start]

        wave_heights.append(H)
        wave_periods.append(T)

    results[location[i]] = {
        'wave_heights': np.array(wave_heights),
        'wave_periods': np.array(wave_periods)
    }

#Example of use of the result: results['Location 3']['wave_periods'] gives the array of wave periods of location 3 in chronological order
#

########################################################################################
#Calculating H1/3


H1_3 = {}
for loc in location:
    sorted = np.sort(results[loc]['wave_heights'])
    n=int(len(sorted)*(2/3))
    H1_3[loc] = {'3rds': np.mean(sorted[n:])}

for loc in location:
    print(f'H1/3 at {loc} = {H1_3[loc]['3rds']:.2f}')


###################################################################################################
#Figures of wave heights.

for i,n,loc in zip(location,range(8),location):
    t=np.cumsum(results[i]['wave_periods'])
    plt.figure(n+10)
    plt.title(f'Wave heights at {i}')
    plt.xlabel('Time [s]')
    plt.ylabel('Wave height [m]')
    plt.hlines(y=H1_3[loc]['3rds'],colors='r',linestyles='-',xmin=t[0],xmax=t[-1],label=f'H1/3 = {H1_3[loc]["3rds"]:.2f}')
    plt.scatter(t,results[i]['wave_heights'],label='Wave heights')
    plt.legend(loc='upper left')
    plt.savefig(f'{location[n]} wave periods scatter plot')



means = {}

for loc,ti in zip(location,time):
    means[loc] = {
        'avg': np.mean(results[loc]['wave_heights'])
    }
    print(f'Aveage wave height at {loc} is {means[loc]["avg"]:.2f}[m] from {ti[0]} to {ti[-1]}')


#
AVGWaveOutside = {}

AVGWaveOutside[location[0]] = { 'AVGWave': 1.93 }
AVGWaveOutside[location[1]] = { 'AVGWave': 1.91 }
AVGWaveOutside[location[2]] = { 'AVGWave': 1.86 }
AVGWaveOutside[location[3]] = { 'AVGWave': 2.18 }
AVGWaveOutside[location[4]] = { 'AVGWave': 2.18 }
AVGWaveOutside[location[5]] = { 'AVGWave': 1.95 }
AVGWaveOutside[location[6]] = { 'AVGWave': 2.11 }
AVGWaveOutside[location[7]] = { 'AVGWave': 1.91 }

Diffraction = {}

for loc in location:
    Diffraction[loc] = {
        'CD': means[loc]['avg'] / AVGWaveOutside[loc]['AVGWave'],
    }
    print(f'Diffraction coefficient for {loc} is {Diffraction[loc]["CD"]:.2f}')

for i,loc in zip(range(8),location):
    plt.figure(i+20)
    plt.title(f'Histogram of wave heights at {loc}')
    plt.hist(results[loc]['wave_heights'],bins=10)
    plt.savefig(f'{location[i]} histogram of wave heights')


##########################################################################
#Creating zooms of raw data and displaying the individual waves (first 60 data points)
dist = [dist1, dist2, dist3, dist4, dist5, dist6, dist7, dist10]

timer=[t1,t2,t3,t4,t5,t6,t7,t10]

for i in range(8):
    plt.figure(i + 30)
    t = timer[i][:60]
    d = dist[i][:60]
    plt.plot(t, d)
    for j in range(len(d) - 1):
        if d[j] >= 0 and d[j + 1] < 0:
            plt.axvline(x=t[j], linestyle='--')
    plt.grid()
    plt.savefig(f'{location[i]} raw data zoom')




########################################################################
#FFT of raw data

for i in range(8):
    N=len(dist[i])
    T=1.0 / 800
    x=timer[i]
    y=dist[i]
    mask=~np.isnan(y)
    x=x[mask]
    y=y[mask]
    yf=fft(y)
    xf=fftfreq(N,T)[:N//2]
    plt.figure(40+i)
    plt.title(f'{location[i]} FFT')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('Amplitude')
    plt.plot(xf,2.0/N*np.abs(yf[0:N//2]))
    plt.grid()
    plt.savefig(f'{location[i]} FFT')


###########################################################################
#Displaying filtering of data.

maxindex={}
for loc,i,dis in zip(location,range(8),dist_unfiltered):
    maxindex[loc]={'max': np.argmax(dis)}
    print(f'Max index of unfiltered dist at {loc} is {maxindex[loc]['max']}')

plt.figure(50)
plt.plot(t2[3200:3260]-t2[0],dist[1][3200:3260],color='blue',label='Filtered data',linewidth=2)
plt.plot(t2[3200:3260]-t2[0],dist_unfiltered[1][3200:3260],color='red',linestyle='--',label='Unfiltered data')
plt.legend(loc='upper right')
plt.xlabel('Time [s]')
plt.ylabel('Distance [m]')
plt.savefig('Unfiltered vs filtered raw data')

#Keep show in bottom
#plt.show() not now baby