import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

# 1. Define the data points for the curve
# X-axis: Mass / Sieve Aperture (arbitrary units based on image labels)
# Y-axis: % by mass less than (passing)
x_data = np.array([0, 10, 15, 30, 45, 60, 75, 90, 100])
y_data = np.array([0, 2, 5, 20, 45, 75, 90, 97, 100])

# Smooth the curve using B-spline interpolation
x_smooth = np.linspace(x_data.min(), x_data.max(), 300)
spl = make_interp_spline(x_data, y_data, k=3)
y_smooth = spl(x_smooth)

# 2. Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_smooth, y_smooth, color='black')

# 3. Add the Grading Requirement Bars (The gray boxes/bars)
# Format: [x_coord, y_min, y_max, label]
requirements = [
    (15, 0, 5, 'ELL'),    # Extreme Lower Limit
    (25, 0, 10, 'NLL'),   # Nominal Lower Limit
    (70, 70, 100, 'NUL'), # Nominal Upper Limit
    (97, 97, 100, 'EUL')  # Extreme Upper Limit
]

for x, ymin, ymax, label in requirements:
    # Draw vertical dashed line
    plt.vlines(x, 0, 105, colors='black', linestyles='dotted', linewidth=1)
    # Add labels at the bottom
    plt.text(x, -5, label, ha='center', fontsize=12, fontweight='bold')
    # Add percentage labels near the bars
    if ymax == 100:
        plt.text(x + 2, ymin, f'{ymin}%', va='top', fontsize=12)
    else:
        plt.text(x - 2, ymax + 2, f'{ymax}%', ha='right', fontsize=12)

# 4. Formatting the axes
plt.xlim(0, 105)
plt.ylim(0, 105)

# Axis Labels
plt.ylabel('% by mass\nless than\n(passing)', rotation=0, labelpad=40, va='center', fontsize=12)
plt.xlabel('Mass / sieve aperture', fontsize=12)

# Remove top and right spines to match image style
ax = plt.gca()
ax.spines['top'].set_visible(True)
ax.spines['right'].set_visible(True)

# Custom Ticks
plt.yticks([0, 100], fontsize=12)
plt.xticks([]) # Hide default numbers to use labels (ELL, NLL, etc.)

plt.tight_layout()
plt.show()