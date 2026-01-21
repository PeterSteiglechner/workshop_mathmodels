# %%
from scipy.integrate import odeint
import numpy as np
import matplotlib.pyplot as plt

a = 0.5  # infection prob 50%
c = 2  # meet 2 random people per day
rho = 0.2  # recovery nearly complete after 14 days
sigma = 0.03  # re-infection (R2S rate) relatively slow
delta = 0.02  # mortality


def sirmodel(sir, t):
    s, i, r = sir
    dsdt = -a * c * s * i + sigma * r
    didt = a * c * s * i - delta * i - rho * i
    drdt = rho * i - sigma * r
    system_deriv = [dsdt, didt, drdt]
    return system_deriv

t = np.linspace(start=0, stop=100, num=101)

i0 = 2 / (80e6)  # initially sick agents
sir0 = np.array([1 - i0, i0, 0.0])
sir = odeint(sirmodel, sir0, t)

# %%
# OBSERVE
plt.plot(t, sir[:, 0], color="grey", label="susceptible")
plt.plot(t, sir[:, 1], color="red", label="infected")
plt.plot(t, sir[:, 2], color="green", label="recovered")
plt.ylabel("fraction of society")
plt.xlabel("time [days]")
plt.ylim(0,)
plt.legend()


#
# %%
