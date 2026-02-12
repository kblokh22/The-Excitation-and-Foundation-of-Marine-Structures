import pandas as pd
import numpy as np
from scipy import stats

# 1. Define the local path to your file
file_path = r"C:\Users\lukac\Desktop\Materials\2 Semestar\Risk and Reliability in Engineering\Exercises\Project\Vejrdata 2018-2025.xlsx"

try:
    # 2. Load the data – use file_path
    df = pd.read_excel(file_path, skiprows=1)

    # 3. Data Cleaning
    df['Tidspunkt'] = pd.to_datetime(df['Tidspunkt'], dayfirst=True, errors='coerce')
    df = df.dropna(subset=['Tidspunkt', 'Mid. bølg [m]'])
    df['Year'] = df['Tidspunkt'].dt.year

    # 4. Extract annual maxima
    annual_max = df.groupby('Year')['Mid. bølg [m]'].max().values
    n = len(annual_max)
    print("Annual maxima:", annual_max)

    # 5. MAXIMUM LIKELIHOOD ESTIMATION (MLE)
    mu_mle, beta_mle = stats.gumbel_r.fit(annual_max)

    # 6. CALCULATE 50-YEAR RETURN LEVEL
    T = 50
    F_50 = 1 - 1/T
    hs_50_mle = stats.gumbel_r.ppf(F_50, loc=mu_mle, scale=beta_mle)

    # 7. RESULTS OUTPUT
    print("\n--- Gumbel Extreme Analysis (Maximum Likelihood Method) ---")
    print(f"MLE Location Parameter (mu): {mu_mle:.4f}")
    print(f"MLE Scale Parameter (beta):  {beta_mle:.4f}")
    print("-" * 58)
    print(f"50-YEAR SIGNIFICANT WAVE HEIGHT (Hs): {hs_50_mle:.2f} m")
    print("-" * 58)

except Exception as e:
    print(f"Error: {e}")
