import pandas as pd
import inspect
import numpy as np
from datetime import datetime, timezone


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


Names=np.array([['t1','dist1','time1'],['t2','dist2','time2']])
DirectoryAndName=np.array([['ultrasonic_data_1_20260325_141647.csv'],['ultrasonic_data_1_20260325_141647.csv']])
Coloumns=np.array([0,1,2])
FirstRow=0

for i in range(2):
    csv_to_vars(Names[:][i], DirectoryAndName[i][0], Coloumns, FirstRow)



for i in range(len(time1)):
    print(datetime.fromtimestamp(int(time1[i]), timezone.utc))