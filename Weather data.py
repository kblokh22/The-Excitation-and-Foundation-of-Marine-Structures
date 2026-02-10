import numpy as np
import pandas as pd

t=np.arange(1, 4079, 1)

df = pd.read_excel("vejrdata/Samlet vejrdata 2013.2019-NK.xlsx",sheet_name='2013')
windspeed2013 = df.iloc[1:, 2].values
print(windspeed2013)


