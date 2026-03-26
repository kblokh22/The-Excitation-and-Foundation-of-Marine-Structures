import pandas as pd
import inspect
import numpy as np
from datetime import datetime, timezone
import matplotlib.pyplot as plt


def csv_to_vars(Names, DirectoryAndName, Coloumns, FirstRow):
    df = pd.read_csv(DirectoryAndName, header=None)
    caller_globals = inspect.currentframe().f_back.f_globals

    for i in range(len(Names)):
        caller_globals[Names[i]] = df.iloc[FirstRow:, Coloumns[i]].values



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


#Converts the time array from unix to real time
for i in range(len(Names)):
    time_array = globals()[Names[i][2]]
    converted = [
        datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        for ts in time_array
    ]
    globals()[Names[i][2]] = np.array(converted)

for i in range(len(Names)):
    plt.figure()
    t = globals()[Names[i][0]]
    dist = globals()[Names[i][1]]
    plt.plot(t,dist)
    plt.show()