import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Setup gas: air with no fuel initially
gas = ct.Solution('gri30.yaml')
gas.TP = 300, ct.one_atm
gas.set_equivalence_ratio(0, fuel='CH4', oxidizer='O2:1, N2:3.76')

# Engine parameters
compression_ratio = 18.0
V_bd = 0.0005  # displacement volume [m^3]
V_c = V_bd / (compression_ratio - 1)  # clearance volume
V_0 = V_bd + V_c  # initial volume
T_init = 300
P_init = ct.one_atm

# Set gas to initial conditions
gas.TP = T_init, P_init

# Make a reactor and define initial volume
reactor = ct.IdealGasReactor(gas)
reactor.volume = V_0

# Create a simulation network
sim = ct.ReactorNet([reactor])

# Crank angle loop: simulate compression → combustion → expansion
n_steps = 720
theta = np.linspace(0, 720, n_steps)  # crank angle [degrees]
V = np.zeros_like(theta)
P = np.zeros_like(theta)
T = np.zeros_like(theta)
NO = np.zeros_like(theta)
CO = np.zeros_like(theta)

# Simple V(θ) profile (single cylinder 4-stroke, symmetric)
def cylinder_volume(theta_deg):
    theta_rad = np.radians(theta_deg)
    r = 0.5  # crank radius ratio
    return V_c + 0.5 * V_bd * (1 - np.cos(theta_rad))

# Simulation loop
for i, angle in enumerate(theta):
    # Update cylinder volume
    reactor.volume = cylinder_volume(angle)
    
    # Inject fuel just before TDC (e.g., at 355°)
    if 355 <= angle <= 360 and gas.X[gas.species_index('CH4')] < 1e-6:
        gas.set_equivalence_ratio(0.06, fuel='CH4', oxidizer='O2:1, N2:3.76')  # lean mix
        reactor.syncState()
    
    sim.advance(sim.time + 1e-5)

    V[i] = reactor.volume
    P[i] = reactor.thermo.P
    T[i] = reactor.thermo.T
    NO[i] = reactor.thermo['NO'].X[0]
    CO[i] = reactor.thermo['CO'].X[0]

# Plot NO and CO (ppm)
# plt.figure(figsize=(10, 5))
# plt.plot(theta, NO * 1e6, label='NO [ppm]')
# plt.plot(theta, CO * 1e6, label='CO [ppm]')
# plt.xlabel('Crank Angle [°]')
# plt.ylabel('Concentration [ppm]')
# plt.title('NO and CO Emissions in Diesel Engine Cycle')
# plt.grid()
# plt.legend()
# plt.tight_layout()
# plt.show()

# Optional: Plot P-V diagram
# plt.figure(figsize=(6, 5))
# plt.plot(V * 1e6, P / 1e5)
# plt.xlabel('Volume [cm³]')
# plt.ylabel('Pressure [bar]')
# plt.title('Diesel Engine P-V Diagram')
# plt.grid()
# plt.tight_layout()
# plt.show()

# Optional: Plot temperature diagram
plt.figure(figsize=(6, 5))
plt.plot(theta, T)
plt.xlabel('Crank Angle [°]')
plt.ylabel('Temperature K')
plt.title('Temperature vs crank angle')
plt.grid()
plt.tight_layout()
plt.show()
