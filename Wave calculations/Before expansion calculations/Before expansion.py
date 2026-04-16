import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

########################################################################################
#Data and plot of raw data
df=pd.read_excel('locations all before.xlsx',header=None,skiprows=2)

locations=['location 1','location 2','location 3','location 4','location 5','location 6','location 7','location 10']

Data={}
coloumns=[1,2,3,4,5,6,7,8]
for loc,col in zip(locations,coloumns):
    Data[loc]={'wave': df.iloc[:, col].astype(float)}

t = np.arange(0, 600.5, 0.5)

plt.figure(1)
for loc in locations:
    plt.plot(t, Data[loc]['wave'],label=loc,linewidth=0.4)
plt.legend(fontsize='small')
plt.grid(True)

################################################################################
#Zero down crossing

results = {}

for i in range(len(locations)):
    eta = Data[locations[i]]['wave'].values
    t_målt = t

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

    results[locations[i]] = {
        'wave_heights': np.array(wave_heights),
        'wave_periods': np.array(wave_periods)
    }

for loc in locations:
    plt.figure()
    x=np.cumsum(results[loc]['wave_periods'])
    y=results[loc]['wave_heights']
    plt.scatter(x,y)
    plt.title(loc)

for i in range(8):
    plt.figure(i+20)
    plt.plot(t, Data[locations[i]]['wave'])

plt.show()


