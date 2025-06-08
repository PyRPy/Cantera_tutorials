import cantera as ct
import matplotlib.pyplot as plt
import numpy as np
# simplified constant pressure for ICE

# Load the GRI-Mech 3.0 mechanism (includes NO and CO reactions)
gas = ct.Solution('gri30.yaml')

# Define initial conditions
T = 1500  # temperature in Kelvin
P = ct.one_atm  # pressure
phi = 1.0  # equivalence ratio (stoichiometric)

# Methane-air mixture
gas.set_equivalence_ratio(phi, fuel='CH4', oxidizer='O2:1, N2:3.76')
gas.TP = T, P

# Create a reactor and reservoir
reactor = ct.IdealGasReactor(gas)
env = ct.Reservoir(gas)

# Connect reactor to environment (simulate constant-pressure reactor)
valve = ct.Valve(reactor, env)
valve.valve_coeff = 1.0

# Reactor network
sim = ct.ReactorNet([reactor])

# Simulation time
time = 0.0
end_time = 1.0  # seconds
dt = 1e-4

# Data storage
times, CO_vals, NO_vals, T_vals = [], [], [], []

while time < end_time:
    time += dt
    sim.advance(time)

    times.append(time)
    CO_vals.append(reactor.thermo['CO'].X[0])
    NO_vals.append(reactor.thermo['NO'].X[0])
    T_vals.append(reactor.thermo.T)

# Convert to numpy arrays for plotting
times = np.array(times)
CO_vals = np.array(CO_vals)
NO_vals = np.array(NO_vals)

# Plot CO and NO mole fractions
plt.figure(figsize=(10, 6))
plt.plot(times, CO_vals * 1e6, label='CO (ppm)')
plt.plot(times, NO_vals * 1e6, label='NO (ppm)')
plt.xlabel('Time [s]')
plt.ylabel('Concentration [ppm]')
plt.title('CO and NO Emissions in PSR')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
