import pandas as pd
import numpy as np

data=pd.read_csv('Weather data/A.3.1. Hirtshals_contours_25cm_Opmåling_2021.txt', sep=' ', header=None, names=["x", "y", "z"])
print(data.head())

data_red = data.iloc[::10000]

print(len(data),len(data_red))

data_red.to_csv("Depth_reduced.xyz",index=False,sep=' ',header=False)