from CPT_Angle_of_friction_3 import avg_phi_per_layer3
from CPT_Angle_of_friction_14 import avg_phi_per_layer14

print(f"Friction angle for CPT3: {avg_phi_per_layer3}")
print(f"Friction angle for CPT14 {avg_phi_per_layer14}")

avg_phi_3 = avg_phi_per_layer3.mean()
avg_phi_14 = avg_phi_per_layer14.mean()

print(f"Friction angle for CPT3: {avg_phi_3:.2f}")
print(f"Friction angle for CPT14 {avg_phi_14:.2f}")