#%% 
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt 

sigma = 10
rho= 28
beta=8/3
def lorenzsystem(s, t):
    x,y,z = s
    dxdt = sigma * (y-x)
    dydt = x * (rho - z) - y
    dzdt = x*y - beta* z
    system_deriv = [dxdt, dydt, dzdt]
    return system_deriv

t = np.linspace(start=0 , stop=30, num=1001)

s0 = np.array([0.9,0.,0.])
s = odeint(lorenzsystem, s0, t)

plt.plot(s[:,0], s[:,1], color="blue", alpha=0.5)

s0 = np.array([1.0,0.,0.])
s = odeint(lorenzsystem, s0, t)

plt.plot(s[:,0], s[:,1], color="red", alpha=0.5)
# %%

#