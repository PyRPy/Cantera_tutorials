import cantera as ct
import numpy as np
import matplotlib.pyplot as plt

# Load mechanism (includes NOx and CO)
gas = ct.Solution('gri30.yaml')

# Initial conditions
T_init = 300  # K
P_init = ct.one_atm
gas.TP = T_init, P_init
gas.set_equivalence_ratio(phi=1.1, fuel='CH4', oxidizer='O2:1.0, N2:3.76')

# Engine parameters
compression_ratio = 18.0
V_bd = 0.0005  # 500 cc engine
V_c = V_bd / (compression_ratio - 1)
V_0 = V_c + V_bd

# Crank angle array
theta = np.linspace(0, 720, 720)
V = lambda th: V_c + 0.5 * V_bd * (1 - np.cos(np.radians(th)))

# Reactor setup
gas.TP = T_init, P_init
reactor = ct.IdealGasReactor(gas)
reactor.volume = V(0)
sim = ct.ReactorNet([reactor])

# Storage arrays
T_hist, P_hist, V_hist, NO_hist, CO_hist = [], [], [], [], []

for i, angle in enumerate(theta):
    reactor.volume = V(angle)

    # Inject fuel near TDC
    if 359 <= angle <= 360:
        gas.set_equivalence_ratio(phi=0.06, fuel='CH4', oxidizer='O2:1, N2:3.76')
        gas.TP = reactor.T, reactor.thermo.P  # Set gas to current conditions
        reactor.syncState()  # Important to update reactor state with new gas!

    sim.advance(sim.time + 1e-5)

    # Save data
    T_hist.append(reactor.thermo.T)
    P_hist.append(reactor.thermo.P)
    V_hist.append(reactor.volume)
    NO_hist.append(reactor.thermo['NO'].X[0])
    CO_hist.append(reactor.thermo['CO'].X[0])

# Convert to numpy arrays
T_hist = np.array(T_hist)
P_hist = np.array(P_hist)
V_hist = np.array(V_hist)
NO_hist = np.array(NO_hist)
CO_hist = np.array(CO_hist)

# === PLOTS ===

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.plot(theta, T_hist)
plt.xlabel('Crank Angle [°]')
plt.ylabel('Temperature [K]')
plt.title('Cylinder Temperature vs Crank Angle')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(theta, CO_hist * 1e6, label='CO [ppm]')
plt.plot(theta, NO_hist * 1e6, label='NO [ppm]')
plt.xlabel('Crank Angle [°]')
plt.ylabel('Concentration [ppm]')
plt.title('Emissions vs Crank Angle')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# P–V diagram
plt.figure()
plt.plot(np.array(V_hist) * 1e6, np.array(P_hist) / 1e5)
plt.xlabel('Volume [cm³]')
plt.ylabel('Pressure [bar]')
plt.title('P–V Diagram of Diesel-like Cycle')
plt.grid(True)
plt.show()
