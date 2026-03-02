import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

B = np.array(['B04', 'B11'])
depth = np.array(['29.53-29.56', '29.53-29.56'])

Q = np.array([0.12,0.26])


sigma_oc_akai = np.array([680,890])
sigma_oc_casa = np.array([600,800])

df = pd.DataFrame()
df['Borehole'] = B
df['Depth [m]'] = depth
df['$Q_(1600-3200)$'] = Q
df['sigma_oc_akai'] = sigma_oc_akai
df['sigma_oc_casa'] = sigma_oc_casa

print(df)





