import numpy as np
from helper_functions import waveLengthIteration, draw_complete_breakwater

GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
PINK = '\033[95m'
RESET = '\033[0m'

# Known values
g = 9.82 # Gravitational acceleration [m/s^2]
h = 10 # Water depth [m]
Hs = 5.84 # Significant wave height [m]
Hm0 = Hs # Significant wave height based on frequency spectrum. That is not used here. [m]
T_10 = 12.7 # Spectral period [s]
Tm = 12.7 # Mean period [s]
Nw = 1000 # Number of waves when checking for damage

# Structure
Dn50 = np.array([1.68, 0.64, 0.2]) # Stone size when looking at the armour layer, filter layer and core. [m]
PermeableStructure = True  # If the breakwater is permeable to water.
Gc = 3 * Dn50[0] # Is the width of the crest. [m]
q_criteria = 10 # The amount of water that is allowed to over-top. [l/s per m]
slope=1/2.5 #top is y bottom is x
slope_angle = np.arctan(slope) # The slope of the breakwater. np.arctan(1/2) = is a slope of 1:2.

t_t=2*Dn50[0] # Height of toe
B_t=3*Dn50[0] # Width of toe

# Thickness of layers
c_thickness = 1 # 1 because of rock armour type
t_armour = 2 * c_thickness * Dn50[0]
t_filter = max(2 * Dn50[1], 0.5 * Dn50[0], 0.5)
Thickness = np.array([t_armour, t_filter]) # Thickness of the armour layer and filter layer. [m]

for idx, thickness in enumerate(Thickness):
    print(f"Thickness of layer {idx+1}: {thickness:.2f}")

# Wave parameters
L_mDeep = (g * Tm**2) / (2 * np.pi)
L_10Deep = (g * T_10**2) / (2 * np.pi)

L_10 = waveLengthIteration(Tm, h)

s_m = Hs / L_mDeep
s_10 = Hm0 / L_10Deep

xi_m = np.tan(slope_angle) / np.sqrt(s_m)
xi_10 = np.tan(slope_angle) / np.sqrt(s_10)

# (1) Overtopping EurOtop
gamma_f = 0.4
beta=0 #angle of attack
gamma_beta = 1-0.0062*beta

if xi_10 > 5:
    gamma_fmod = min(gamma_f + (xi_10 - 5) * (1 - gamma_f) / 5, 1)
    if PermeableStructure:
        gamma_fmod = min(gamma_fmod, 0.6)
else:
    gamma_fmod = gamma_f

q = 10000000.0 #initialize
R_c = 0.0      #initialize
while q - q_criteria > 1e-9:
    q = (0.09 * np.exp(-(1.5 * R_c / (Hm0 * gamma_fmod * gamma_beta))**1.3)) * np.sqrt(g * Hm0**3) * 1000
    R_c += 0.00001

R_cEurOtop = R_c
print(f"R_cEurOtop: {R_cEurOtop:.4f}")

# (2) Overtopping Eldrup
gamma_fS = min(gamma_f + 0.05 * s_10**-0.5 - 0.07 * min(1/np.tan(slope_angle), 3) - 0.09, 1)
Gcstar = Gc
gamma_cw = min(1.1 * np.exp(-0.18 * Gcstar / Hm0), 1)

q = 10000000.0
R_c = 0.0
while q - q_criteria > 1e-9:
    q = (0.09 * np.exp(-(1.5 * R_c / (Hm0 * gamma_fS * gamma_beta * gamma_cw))**1.3)) * np.sqrt(g * Hm0**3) * 1000
    R_c += 0.00001

R_cEldrup = R_c
print(f"R_cEldrup: {R_cEldrup:.4f}")

# (3) P-Estimation
N = len(Dn50)
zstar1 = np.zeros(N)
zstar2 = np.zeros(N)

for i in range(N):
    if i == 0:
        zstar1[i] = 0
        zstar2[i] = Thickness[i] / Dn50[0]
    elif i == N - 1:
        zstar1[i] = Thickness[i-1] / Dn50[0] + zstar1[i-1]
        zstar2[i] = 13
    else:
        zstar1[i] = Thickness[i-1] / Dn50[0] + zstar1[i-1]
        zstar2[i] = Thickness[i] / Dn50[0] + zstar2[i-1]

k_vals = (0.79 - 0.79 * np.exp(-4.1 * Dn50 / Dn50[0])) * ((np.exp(-0.62 * zstar1) - np.exp(-0.62 * zstar2)) / 0.62)
P = max(0.1, 1.72 * np.sum(k_vals) - 1.58)
print(f"P: {P:.4f}")

# (4) Sd
gamma_a = 2650*9.82
gamma_w = 1025*9.82
Delta = (gamma_a / gamma_w - 1)
Dn50_A = Dn50[0]

xi_criteria = (6.2 * P**0.31 * np.sqrt(np.tan(slope_angle)))**(1 / (P + 0.5))

if xi_m < xi_criteria:
    S = (Hs / (Delta * Dn50_A * 6.2 * P**0.18 * xi_m**-0.5))**(1 / 0.2) * np.sqrt(Nw)
else:
    cot_alpha = 1 / np.tan(slope_angle)
    S = (Hs / (Delta * Dn50_A * 1 * P**-0.13 * xi_m**P * np.sqrt(cot_alpha)))**(1 / 0.2) * np.sqrt(Nw)

print(f"S: {S:.4f}")
if S < 2:
    print(f"{GREEN}The breakwater sustains initial damage.{RESET}\n")
elif 4 <= S <= 6:
    print(f"{GREEN}The breakwater sustains intermediate damage.{RESET}\n")
elif S >= 8:
    print(f"{RED}The breakwater leads to failure. The filter layer is exposed.{RESET}\n")
else:
    print(f"{YELLOW}The breakwater is transitioning/intermediate state.{RESET}\n")

# (5) Toe Damage
tt = 2 * Dn50_A
ht = h - tt
Bt = 3 * Dn50_A
k_toe = 2 * np.pi / (g * T_10**2 / (2 * np.pi))
udelta = np.pi * Hs / T_10 * 1 / np.sinh(k_toe * ht)
Nod = 0.032 * (tt / Hs) * (Bt / Hs)**0.3 * (Hs / (Delta * Dn50_A))**3 * (udelta / np.sqrt(g * Hs))
print(f"Nod: {Nod:.4f}") # Also done later

# (6) Reflection
KR0, KR1 = 0.2, 0.8
gamma_refl = 3.55
a_refl = 0.18
Cr = (KR1 - KR0) * (1 + ((h / (L_10 * np.tan(slope_angle))) / a_refl)**gamma_refl)**-1 + KR0
print(f"Cr: {Cr:.4f}")

# (7) Transmission
b_trans = -5.42 * s_m + 0.0323 * Hs / Dn50_A - 0.0017 * (Gc / Dn50_A)**1.84 + 0.51
Ct = (0.031 * Hs / Dn50_A - 0.24) * R_cEurOtop / Dn50_A + b_trans
Ct = np.clip(Ct, 0.075, 0.75)
print(f"Ct: {Ct:.4f}\n")

#Scour (slope 1:2 is safe)
#For a breakwater with a front slope of 1:1.2 the scour protection should cover 0.15L of the seabed and for a slope of 1:1.75 the scour should cover 0.08L.

''' 
#Scour
alpha=slope_angle*360/(2*np.pi)

def f_alpha(alpha):
    f=0.3-1.77*np.exp(-alpha/15)
    return f

S=0.0001

f=f_alpha(alpha)
print(f'f={f}')
while S/Hs <= f / (( np.sinh(2*np.pi*h/L_10) )**1.35):
    S=S+0.0001

print(f'The breakwater scour is {S}')
'''

#Stability
Ns=Hs / (Delta*Dn50[0])

dn50_max = Hs / (Delta * 1)

dn50_min = Hs / (Delta * 4)

print(f"Dn50 must be between {dn50_min:.3f} m and {dn50_max:.3f} m")
print(f'The armour unit Dn50A is {Dn50[0]} m')
if dn50_min < Dn50[0] < dn50_max:
    print(f'{GREEN}The stone size fits the requirement{RESET}\n')
else:
    print(f'{RED}The stone size does not fit the requirement{RESET}\n')

print("Ns must be between 1 and 4")
print(f'Ns: {Ns:.4f}')
if 1 < Ns < 4:
    print(f'{GREEN}Rubble-mound is stable{RESET}\n')
else:
    print(f'{RED}Rubble-mound is unstable{RESET}\n')


#Sliding
C=1 # guess so far
rho_a=gamma_a/9.82
rho_w=gamma_w/9.82
H=Hs
KD=3 #made from rocks

alpha=slope_angle
print(f'slope_angle: {slope_angle:.4f}')

def cot(x):
    cotan=1/np.tan(x)
    return cotan

M=(rho_a*H**3) / (KD*(rho_a/rho_w - 1)**3 * cot(alpha))
mu=0.7
side1=(rho_a*H**3) / (M*(rho_a/rho_w - 1)**3 * cot(alpha))
side2=(1/(C**3 * cot(alpha)))*( (mu*np.cos(alpha)-np.sin(alpha))/(np.cos(beta)+mu*np.sin(beta)) )**3

print(f'side1: {side1}')
print(f'side2: {side2}')
if side1 <= side2:
    print(f"{GREEN}No sliding occurs{RESET}\n")
elif side1 > side2:
    print(f'{RED}Sliding occurs{RESET}\n')
elif side1 < 0:
    print('Negative result (error)\n')

#Toe stability
T_m1=T_10
h_t=h-t_t

k=2*np.pi / (g/(2*np.pi) * T_m1**2)
mu_s=(np.pi*Hs) / T_m1 * 1 / np.sinh(k*h_t)
N_OD=0.032*(t_t/Hs)*(B_t/Hs)**0.3 * (Hs/(Delta*Dn50[0]))**3 * (mu_s/np.sqrt(9.82*Hs))
print(f"N_OD: {N_OD:.2f}")
if N_OD < 0.5:
    print(f"{GREEN}Toe stability leads to initial damage.{RESET}\n")
elif 2 <= N_OD <= 3:
    print(f"{GREEN}Toe stability leads to moderate to severe damage. This is often used as a design criterion.{RESET}\n")
elif N_OD >= 5:
    print(f"{RED}Toe stability leads to failure.{RESET}\n")
else:
    print(f"{YELLOW}Toe stability is transitioning/intermediate state.{RESET}\n")


# Stability of the roundhead

A_round = 0.198
B_round = -1.234
C_round = 3.289

required_stone_size = (A_round * xi_m**2 + B_round * xi_m + C_round) / Hs

print(f"Stone size required for roundhead stability: {required_stone_size:.4f} m")

if required_stone_size <= Dn50[0]:
    print(f"{GREEN}Roundhead is stable with stone size {Dn50[0]:.2f} m{RESET}")
else:
    print(f"{RED}Roundhead is unstable with stone size {Dn50[0]:.2f} m{RESET}")

'''
# Thickness of the layers according to the US army coastal engineering manual
# (Page VI-5-135)

# Conversion from weight to diameter

n = 2           # number of quarrystone
k_delta = 1     # Layer coefficient
w_a = rho_a      # Specific weight of the quarrystone
D_sieve = np.array([1.68, 0.93])     # Diameter of the stone to be investigated
W = 0.6575162324 * w_a * D_sieve**3         # weight of the individual quarrystone

for idx, W_i in enumerate(W):
    print(f"Weight of layer {idx+1}: {W_i:.4f}")

r = n * k_delta * ( W / w_a )**(1/3)

for idx, r_i in enumerate(r):
    print(f"Thickness of layer {idx+1}: {r_i:.4f}")
'''

measurements = {
    'water_depth': h,
    'crest_height_above_seabed': h + R_cEldrup + Thickness[0],
    'crest_width': Gc,
    'slope_seaward': 1/slope,
    'slope_landward': 1/slope,
    'armour_thickness': Thickness[0],
    'filter_thickness': Thickness[1],
    'toe_width': B_t,
    'toe_height': t_t
}

draw_complete_breakwater(measurements)