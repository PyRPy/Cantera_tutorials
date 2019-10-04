#!/usr/bin/env python
# coding: utf-8

# In[1]:


"""
A Rankine vapor power cycle
"""


# In[2]:


import cantera as ct


# In[3]:


# parameters
eta_pump = 0.6 # isentropic eff
eta_turbine = 0.8
p_max = 8.0e5


# In[10]:


def pump(fluid, p_final, eta):
    """Adiabatically pump a fluid to pressure p_final, using
    a pump with isoentropic efficiency eta.
    """
    h0 = fluid.h
    s0 = fluid.s
    fluid.SP = s0, p_final
    h1s = fluid.h
    isentropic_work = h1s - h0
    actual_work = isentropic_work / eta
    h1 = h0 + actual_work
    fluid.HP = h1, p_final
    return actual_work


# In[5]:


def expand(fluid, p_final, eta):
    """Adiabatically expand a fluid to pressure p_final, using
    a turbine with isentropic efficiency eta."""
    h0 = fluid.h
    s0 = fluid.s
    fluid.SP =s0, p_final
    h1s = fluid.h
    isentropic_work = h0 - h1s
    actual_work = isentropic_work * eta
    h1 = h0 - actual_work
    fluid.HP = h1, p_final
    return actual_work


# In[6]:


def printState(n, fluid):
    print('\n***************** State {0} ******************'.format(n))
    print(fluid.report())


# In[7]:


# create an object representing water
w = ct.Water()


# In[8]:


# start with saturated liquid water at 300 K
w.TX = 300.0, 0.0
h1 = w.h
p1 = w.P
printState(1, w)


# In[11]:


# pump it adiabatically to p_max
pump_work = pump(w, p_max, eta_pump)
h2 = w.h
printState(2, w)


# In[12]:


# heat it at constant pressure until it reaches the saturated vapor state
# at this pressure
w.PX = p_max, 1.0
h3 = w.h
heat_added = h3 - h2
printState(3, w)


# In[13]:


# expand back to p1
turbine_work = expand(w, p1, eta_turbine)
printState(4, w)


# In[14]:


turbine_work


# In[15]:


# efficiency
eff = (turbine_work - pump_work)/heat_added
print('efficiency = ', eff)


# In[ ]:


# https://cantera.org/examples/python/thermo/rankine.py.html

