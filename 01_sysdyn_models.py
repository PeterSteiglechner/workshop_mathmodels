#%% 
import numpy as np
import matplotlib.pyplot as plt

def derivative(y , t):
   dydt = -0.2 * y
   return dydt


from scipy.integrate import odeint
t = np.linspace(start=0 , stop=40.0, num=401)
y0 = 1.0
y = odeint(derivative, y0, t)


# %%

plt.plot(t, y)



# %%
