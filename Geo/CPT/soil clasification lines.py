import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 8))

# Center of the concentric circles for the Robertson 1990 equation
log_Fr_c = -1.22
log_Qt_c = 3.47

# The Ic boundaries defining the soil zones
Ic_boundaries = [1.31, 2.05, 2.60, 2.95, 3.60]

# Generate parametric circles for each boundary
theta = np.linspace(0, 2 * np.pi, 1000)

for Ic in Ic_boundaries:
    # Calculate log values using circle parameters
    log_Fr = log_Fr_c + Ic * np.cos(theta)
    log_Qt = log_Qt_c + Ic * np.sin(theta)

    # Convert back to linear space for the log-log plot
    Fr = 10 ** log_Fr
    Qt = 10 ** log_Qt

    # Plot the boundaries (the plot limits will crop the full circles automatically)
    ax.plot(Fr, Qt, 'k-', linewidth=1.5)

# Add text labels roughly in the center of the zones
ax.text(0.3, 300, '7: Gravelly\nSand', fontsize=10, fontweight='bold', ha='center')
ax.text(0.8, 80, '6: Sands', fontsize=10, fontweight='bold', ha='center')
ax.text(1.5, 30, '5: Sand Mixtures', fontsize=10, fontweight='bold', ha='center')
ax.text(2.5, 12, '4: Silt Mixtures', fontsize=10, fontweight='bold', ha='center')
ax.text(4.5, 5, '3: Clays', fontsize=10, fontweight='bold', ha='center')
ax.text(7.0, 1.5, '2: Organic\nSoils', fontsize=10, fontweight='bold', ha='center')

# Format the plot with Log-Log scales
ax.set_xscale('log')
ax.set_yscale('log')

# Set typical limits for CPT Robertson charts
ax.set_xlim(0.1, 10)
ax.set_ylim(1, 1000)

# Add Labels and Title
ax.set_xlabel('Normalized Friction Ratio, $F_r$ (%)', fontsize=12)
ax.set_ylabel('Normalized Cone Resistance, $Q_t$', fontsize=12)
ax.set_title('Robertson (1990) CPT Soil Behavior Type (SBT) Chart', fontsize=14, pad=15)

# Add grid lines
ax.grid(True, which="major", ls="-", color='gray', alpha=0.5)
ax.grid(True, which="minor", ls="--", color='lightgray', alpha=0.5)

# Show the plot
plt.show()