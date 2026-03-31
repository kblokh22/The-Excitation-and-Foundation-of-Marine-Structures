import numpy as np
import pandas as pd
import inspect
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def csv_to_vars(var_names, file_path, columns, first_row):
    df = pd.read_csv(file_path, header=None, sep=';', decimal=',')
    caller_globals = inspect.currentframe().f_back.f_globals

    for i in range(len(var_names)):
        col_idx = columns[i]
        data = df.iloc[first_row:, col_idx].to_numpy(copy=True)
        try:
            data = data.astype(float)
        except:
            pass

        caller_globals[var_names[i]] = data

Names = [
    ['timeT', 'period'],
    ['timeANGLE', 'angle'],
    ['timeHMAX', 'HMAX'],
    ['timeMEANH', 'MEANH'],
    ['timeMEANWINDSPEED', 'MEANWINDSPEED'],
    ['timeWINDANGLE', 'WINDANGLE'],
    ['timeGUST', 'GUST']
]

Files = [
    'HIS - Bølgeperiode [s].txt',
    'HIS - Bølgeretning [°].txt',
    'HIS - Max Bølgehøjde [m].txt',
    'HIS - Middel Bølgehøjde [m].txt',
    'HIS - Vindhastighed middel [m_s].txt',
    'HIS - Vindretning middel [°].txt',
    'HIS - Vindstød [m_s].txt'
]

Coloumns = [0, 1]
FirstRow = 0

for i in range(len(Names)):
    csv_to_vars(Names[i], Files[i], Coloumns, FirstRow)


#print(timeHMAX[157]) #We arrive at hirtshals and start measuring
#print(timeHMAX[165]) #We leave

plt.figure(1)
plt.plot(timeMEANH[157:165],MEANH[157:165])
plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=3))
plt.show()

