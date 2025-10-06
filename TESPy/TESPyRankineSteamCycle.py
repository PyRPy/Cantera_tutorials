# Simple Rankine Steam Cycle using TESPy
# ------------------------------------------------
# Requirements: pip install tespy
# ------------------------------------------------

from tespy.components import Sink, Source, Pump, Turbine, Condenser, Boiler
from tespy.connections import Connection
from tespy.networks import Network

# --- 1. Define the network ---
steam_cycle = Network(fluids=['water'])
steam_cycle.set_attr(T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

# --- 2. Components ---
# Sources & sinks
water_source = Source('feedwater source')
steam_sink = Sink('steam outlet')

# Main components
pump = Pump('Feedwater Pump')
boiler = Boiler('Boiler')
turbine = Turbine('Steam Turbine')
condenser = Condenser('Condenser')

# --- 3. Connections ---
# Feedwater line
c1 = Connection(water_source, 'out1', pump, 'in1', label='1')
c2 = Connection(pump, 'out1', boiler, 'in1', label='2')
c3 = Connection(boiler, 'out1', turbine, 'in1', label='3')
c4 = Connection(turbine, 'out1', condenser, 'in1', label='4')
c5 = Connection(condenser, 'out1', steam_sink, 'in1', label='5')

steam_cycle.add_conns(c1, c2, c3, c4, c5)

# --- 4. Component parameters ---
# Pump: isentropic efficiency
pump.set_attr(eta_s=0.85)

# Turbine: isentropic efficiency
turbine.set_attr(eta_s=0.85)

# Boiler: set pressure outlet
boiler.set_attr(pr=0.99)  # small pressure drop
# Condenser: set pressure outlet
condenser.set_attr(pr=0.98, t_cond_out=30)  # 30°C condensate

# --- 5. Connection parameters ---
# c1.set_attr(p=0.1, T=30)       # Condenser outlet conditions
# need to fix the problem with pump kW
c1.set_attr(p=0.1, T=30, m=50)  # 50 kg/s feedwater

c3.set_attr(p=80)              # Boiler outlet pressure (high-pressure steam)
c3.set_attr(x=1)               # Dry saturated steam at turbine inlet
c5.set_attr(p=0.1, T=30)       # Condenser outlet (liquid water)
c1.set_attr(fluid={'water': 1})

# --- 6. Solve the network ---
steam_cycle.solve(mode='design')
steam_cycle.print_results()

# --- 7. Calculate efficiency ---
pump_power = pump.P.val  # [W]
turbine_power = turbine.P.val  # [W]
boiler_heat = boiler.Q.val  # [W]
condenser_heat = condenser.Q.val  # [W]

thermal_efficiency = turbine_power / boiler_heat

print("\n--- Rankine Cycle Performance ---")
print(f"Turbine Power: {turbine_power/1e6:.3f} MW")
print(f"Pump Power: {pump_power/1e3:.3f} kW")
print(f"Boiler Heat Input: {boiler_heat/1e6:.3f} MW")
print(f"Condenser Heat Rejection: {condenser_heat/1e6:.3f} MW")
print(f"Cycle Thermal Efficiency: {thermal_efficiency*100:.2f} %")
