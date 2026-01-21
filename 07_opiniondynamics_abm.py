#%%
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import networkx as nx

class agent:
    def __init__(self, id):
        self.id = id
        self.op = np.random.random()   # init: random between 0 and 1

def initialise(params):
    n = params["n"]
    agents = []
    for i in range(n):
        ag = agent(i)  # defining an object of class agent
        agents.append(ag)
    return agents


def update(t, agents, params):
    ag1, ag2 = np.random.choice(agents, size=2, replace=False)
    new_op = (ag1.op + ag2.op)/2
    ag1.op = new_op
    ag2.op = new_op
    return agents

def observe(t, agents):
    snap = [[t, ag.id, ag.op] for ag in agents]
    return snap


# Main
if __name__ == "__main__":
    t = 0
    T = 1000
    times = np.arange(0,T, step=1)
    params = dict(n=200, seed=2026)
    np.random.seed(params["seed"])
    # Main Loop
    agents = initialise(params)
    results = observe(t, agents)
    for t in range(1, T):
        agents = update(t, agents, params)
        results.extend(observe(t, agents))
    df = pd.DataFrame(results, columns=["t","agent_id", "opinion"])

# %%
# ----------------------------------------------
# -------    PLOT EXAMPLE
# ----------------------------------------------

import seaborn as sns
plt.plot([],[],"-",label="agent", color="k")
plt.legend()
sns.lineplot(df, x="t", y="opinion", hue="agent_id",  palette="flare",legend=False)
plt.xlim(0,)

# %%
