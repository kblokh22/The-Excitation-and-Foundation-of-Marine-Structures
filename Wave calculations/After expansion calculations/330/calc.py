import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_excel('wave dist 330.xlsx',skiprows=1)

locations=['loc 1','loc 2','loc 3','loc 4','loc 5','loc 6','loc 7','loc 10']

dist={}
for i in [1,2,3,4,5,6,7,8]:
    dist[locations[i-1]]=df.iloc[:,i]
print(dist)

t=np.arange(0,len(dist[locations[0]]),1)

plt.figure()
for loc in locations:
    plt.plot(t,dist[loc],label=f'{loc}')
plt.legend(prop={'size': 8})
plt.xlabel('Time [s]')
plt.ylabel('Diffraction coefficient [-]')
plt.savefig(f'raw dist coeff.png')



idx=int(len(dist[locations[0]])*(23/30))
print(idx)
stable={}
for loc in locations:
    stable[loc]=dist[loc][idx:]

dist_coeff={}
for loc in locations:
    dist_coeff[loc]=np.mean(stable[loc])

plt.figure()
for loc in locations:
    plt.plot(t[idx:len(t)],stable[loc],label=f'{loc}')
plt.legend(prop={'size': 8})
plt.xlabel('Time [s]')
plt.ylabel('Diffraction coefficient [-]')
plt.savefig(f'stable dist coeff.png')

