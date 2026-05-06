import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df=pd.read_excel('after 290.xlsx',skiprows=1)

locations=['entrance']

dist={}
for i in [1]:
    dist[locations[i-1]]=df.iloc[:,i]
print(dist)

t=np.arange(0,len(dist[locations[0]]),1)

plt.figure()
for loc in locations:
    plt.plot(t,dist[loc],label=f'{loc} Diffraction coefficient')
plt.legend(prop={'size': 8})
plt.xlabel('time [s]')
plt.ylabel('Diffraction Coefficient [-]')
plt.savefig(f'raw dist coeff.png',bbox_inches='tight')



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
plt.ylim([0,2*dist_coeff[locations[0]]])
plt.xlabel('Time [s]')
plt.ylabel('Diffraction Coefficient [-]')
plt.savefig(f'stable dist coeff.png',bbox_inches='tight')

