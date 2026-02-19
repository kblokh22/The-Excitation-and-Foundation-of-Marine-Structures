import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# the values are found by looking at the graphs
q_4 = 190 # kPa
q_5 = 480
q_8 = 420
q_11  = 600

varep_1_4 = 0.15
varep_1_5 = 0.15
varep_1_8 = 0.05
varep_1_11 = 0.15

c_u_4 = 190/2
c_u_5 = 480/2
c_u_8 = 420/2
c_u_11 = 600/2



print("-"*100)
print(" "*45, "results"," "*45)
print("-"*100)
print(f"Undrained shear strength for B4: {c_u_4}")
print(f"Undrained shear strength for B5: {c_u_5}")
print(f"Undrained shear strength for B8: {c_u_8}")
print(f"Undrained shear strength for B11: {c_u_11}")
print("-"*100)
print(f"Undrained deformation B4: {varep_1_4}")
print(f"Undrained deformation B5: {varep_1_5}")
print(f"Undrained deformation B8: {varep_1_8}")
print(f"Undrained deformation B11: {varep_1_11}")
print("-"*100)
