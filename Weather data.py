import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("vejrdata/Vejrdata 2018-2025.xlsx",sheet_name='Vejrdata 2018-2025')
windspeed = df.iloc[2:, 2].values
windspeed=windspeed.astype(float)
print(windspeed)

time=df.iloc[2:, 0].values
print(time)

z=15 #height of the measurement equipment of the wind



