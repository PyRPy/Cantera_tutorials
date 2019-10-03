#!/usr/bin/env python
# coding: utf-8

# In[3]:


# https://cantera.org/examples/jupyter/thermo/heating_value.ipynb.html


# ## Heating value of Methane

# In[1]:


import cantera as ct
gas = ct.Solution('gri30.cti')

# Set reactants state
gas.TPX = 298, 101325, 'CH4:1, O2:2'
h1 = gas.enthalpy_mass
Y_CH4 = gas['CH4'].Y[0] # returns an array, of which we only want the first element

# set state to complete combustion products without changing T or P
gas.TPX = None, None, 'CO2:1, H2O:2' 
h2 = gas.enthalpy_mass

print('LHV = {:.3f} MJ/kg'.format(-(h2-h1)/Y_CH4/1e6)) # LHV


# In[2]:


# get the HHV including heat in water vapor
water = ct.Water()
# Set liquid water state, with vapor fraction x = 0
water.TX = 298, 0
h_liquid = water.h
# Set gaseous water state, with vapor fraction x = 1
water.TX = 298, 1
h_gas = water.h

# Calculate higher heating value
Y_H2O = gas['H2O'].Y[0]
print('HHV = {:.3f} MJ/kg'.format(-(h2 - h1 + (h_liquid - h_gas)*Y_H2O)/Y_CH4/1e6))


# ## Generalizing to arbitrary species

# In[4]:


def heating_value(fuel):
    """ Return the LHV and HHV for the specified fuel or fuel mixture """
    gas.TP = 298, ct.one_atm
    gas.set_equivalence_ratio(1.0, fuel, 'O2:1.0')
    h1 = gas.enthalpy_mass
    Y_fuel = gas[fuel].Y[0]
    
    # complete combustion products
    Y_products = {'CO2': gas.elemental_mole_fraction('C'),
                 'H2O': 0.5 * gas.elemental_mole_fraction('H'),
                 'N2': 0.5 * gas.elemental_mole_fraction('N')}
    
    gas.TPX = None, None, Y_products
    Y_H2O = gas['H2O'].Y[0]
    h2 = gas.enthalpy_mass
    LHV = -(h2 - h1)/Y_fuel
    HHV = -(h2 - h1 + (h_liquid - h_gas)*Y_H2O)/Y_fuel
    return LHV, HHV


# In[8]:


fuels = ['H2', 'CH4', 'C2H6', 'C3H8', 'NH3', 'CH3OH']
print('fuel   LHV (MJ/kg)   HHV (MJ/kg)')
for fuel in fuels:
    LHV, HHV = heating_value(fuel)
    print('{:8s} {:7.3f}     {:7.3f}'.format(fuel, LHV/1e6, HHV/1e6))

