from CPT_Angle_of_friction_3 import phi_peak_KM3
from CPT_Angle_of_friction_14 import phi_peak_KM14
import pandas as pd
import numpy as np
import scipy.stats as stats
df = pd.DataFrame()

# Now these will work:
df['phi_peak_KM14'] = phi_peak_KM14
df['phi_peak_KM3'] = phi_peak_KM3

# Combine them (Assuming these are strings)
phi_combined = pd.concat([df['phi_peak_KM14'], df['phi_peak_KM3']], ignore_index=True)

# Hvis du vil gemme det i et nyt DataFrame
df_phi = pd.DataFrame({'phi_peak_total': phi_combined})

phi_mu = np.mean(df_phi)
phi_std = np.std(df_phi)
phi_c = stats.norm.ppf(0.05, loc=phi_mu, scale=phi_std)
phi_d = np.degrees(np.arctan(np.tan(np.radians(phi_c)) / 1.2))





print(phi_c)
print(phi_d)

