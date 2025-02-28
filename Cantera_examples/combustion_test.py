import numpy as np 
import cantera as ct

gas1 = ct.Solution('gri30.yaml') # gas is 100% hydrogen
gas1()