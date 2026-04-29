import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import grid

date = np.array([0,5,10,20,21,22,36])
p_excess = np.array([-0,-40,-79,-106,-18,-11,-0.9])


plt.figure()
plt.plot(date,p_excess)
plt.xlabel('Date [Day]')
plt.ylabel('P_excess [kPa]')
plt.title('P_excess vs Date')
plt.grid(True, alpha=0.3)
plt.show()


date = np.array([0,5,10,15,20,25,30,36])
u = np.array([0,0.024,0.052,0.084,0.124,0.2,0.228,0.242])
umm = u * 1000

plt.figure()
plt.plot(date,u)
plt.xlabel('Date [Day]')
plt.ylabel('U [mm]')
plt.title('U vs Date')
plt.grid(True, alpha=0.3)
plt.show()