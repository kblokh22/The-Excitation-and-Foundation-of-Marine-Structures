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