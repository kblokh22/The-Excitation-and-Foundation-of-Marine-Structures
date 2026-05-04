import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid

date = np.array([0,20,20.5,21,22,26,33,48,70,93,108])
p_excess = np.array([0,121,99,91,80,68,54,37,21,12,10])
p_excess = p_excess * (-1)


plt.figure()
plt.plot(date,p_excess,color='red')
plt.scatter(date,p_excess,color='red')
plt.xlabel('Date [Day]')
plt.ylabel('P_excess [kPa]')
plt.title('B1: P_excess vs Date')
plt.grid(True, alpha=0.3)


date = np.array([0,20,21,24,30,35,42,50,60,71,81,112])
p_excess = np.array([0,166,153,142,115,100,80,65,50,37,30,15])
p_excess = p_excess * (-1)


plt.figure()
plt.plot(date,p_excess,color='blue')
plt.scatter(date,p_excess,color='blue')
plt.xlabel('Date [Day]')
plt.ylabel('P_excess [kPa]')
plt.title('B2: P_excess vs Date')
plt.grid(True, alpha=0.3)




date = np.array([0,20,21,22,24,26,33,48,63,78,93,108])
u = np.array([0,58,65,67,71,75,84,95,103,107,110,112])

plt.figure()
plt.plot(date,u,color='red')
plt.scatter(date,u,color='red')
plt.xlabel('Date [Day]')
plt.ylabel('U [mm]')
plt.title('B1: U vs Date')
plt.grid(True, alpha=0.3)


date = np.array([0,20,22,32,42,55,66,86,112])
u = np.array([0,88,111,148,169,187,196,207,212])

plt.figure()
plt.plot(date,u,color='blue')
plt.scatter(date,u,color='blue')
plt.xlabel('Date [Day]')
plt.ylabel('U [mm]')
plt.title('B2: U vs Date')
plt.grid(True, alpha=0.3)


x = np.linspace(0,50,2)
y = 2.2*x+11.64
x1 = np.array([29.53,19.31])
E = np.array([76.59,54.11])

plt.figure()
plt.scatter(x1,E,color='red')
plt.plot(x,y,color='blue')
plt.xlabel('E [MPa]')
plt.ylabel('Depth [mm]')
plt.title('Interpolation of E')
plt.grid(True, alpha=0.3)

plt.show()

