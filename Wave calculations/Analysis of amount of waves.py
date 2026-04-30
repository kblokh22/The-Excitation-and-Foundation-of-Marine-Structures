from helper_functions import *

peak_dates, peak_values, filtered_dates, filtered_waves = load_wave_data("Weather data/Samlet vejrdata 2013.2019-NK.xlsx", "Weather data/Vejrdata 2018-2025.xlsx")
df_full = pd.DataFrame({'dato': filtered_dates, 'hoejde': filtered_waves})

results = []

for peak_dt, peak_val in zip(peak_dates, peak_values):
    # 1. Definer et vindue for stormen (f.eks. 24 timer før og efter peak)
    start_storm = peak_dt - pd.Timedelta(hours=24)
    end_storm = peak_dt + pd.Timedelta(hours=24)

    # 2. Udtræk data for denne specifikke storm
    storm_period = df_full[(df_full['dato'] >= start_storm) & (df_full['dato'] <= end_storm)]

    # 3. Find 95% fraktilen for denne storm
    q95 = storm_period['hoejde'].quantile(0.95)

    # 4. Find antallet af bølger/målinger mellem q95 og peak_val
    # Vi tæller alle målinger i stormperioden, der er > q95 (og <= peak_val)
    count_between = storm_period[(storm_period['hoejde'] > q95) & (storm_period['hoejde'] <= peak_val)].shape[0]

    results.append({
        'Peak Dato': peak_dt,
        'Max Hoejde': peak_val,
        '95% Hoejde': q95,
        'Antal over 95%': count_between
    })

# Vis resultaterne
df_results = pd.DataFrame(results)
print(df_results)