# %%
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class agent:
    def __init__(self, id, type, x, y, tolerance):
        self.id = id
        self.type = type
        self.x = x
        self.y = y
        self.tolerance = tolerance
        return

    def update(self, agents, r):
        """check if ratio of similar neighbours is above threshold, otherwise move"""
        # list comprehension method for checking if agents are close enough to the focal agent
        neighbours = [
            nb
            for nb in agents
            if (self.x - nb.x) ** 2 + (self.y - nb.y) ** 2 < r**2 and nb != self
        ]
        if len(neighbours) > 0:
            ratio_similar_neighbours = len(
                [nb for nb in neighbours if nb.type == self.type]
            ) / len(neighbours)
            if ratio_similar_neighbours < self.tolerance:
                self.x = np.random.random()
                self.y = np.random.random()
        return


# generate a population of agents
def initialize(params):
    agents = []
    for i in range(params["n"]):
        type = np.random.choice([0, 1])
        x = np.random.random()
        y = np.random.random()
        ag = agent(i, type, x, y, params["tolerance"])
        agents.append(ag)
    return agents


def update(t, agents, params):
    for i in range(len(agents)):
        ag = np.random.choice(agents)
        ag.update(agents, params["r"])
    return agents


def observe(t, agents):
    snap = [[t, ag.id, ag.type, ag.x, ag.y] for ag in agents]
    return snap


def plot(t, agents):
    reds = [ag for ag in agents if ag.type == 0]
    blues = [ag for ag in agents if ag.type == 1]
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot([ag.x for ag in reds], [ag.y for ag in reds], "o", mfc="red", mec="black")
    ax.plot(
        [ag.x for ag in blues], [ag.y for ag in blues], "o", mfc="blue", mec="black"
    )
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    ax.set_aspect("equal")  # x and y axis should have equal lengths
    ax.set_title(f"Time {int(t)}")
    plt.savefig(f"schelling_figs/{int(t)}.png")
    return


if __name__ == "__main__":
    t = 0
    T = 20
    time_array = np.arange(0, T + 1)
    params = dict(
        n=1000,  # number of agents
        r=0.15,  # neighbourhood radius
        tolerance=0.6,  # min similarity threshold for staying
    )
    if not os.path.isdir("schelling_figs"):
        os.mkdir("schelling_figs")
    agents = initialize(params)
    plot(t, agents)
    results = observe(t, agents)
    for t in time_array[1:]:
        agents = update(t, agents, params)
        if (t % 1) == 0:
            results.extend(observe(t, agents))
            plot(t, agents)
    results = pd.DataFrame(results, columns=["t", "id", "type", "x", "y"])
    results.attrs.update(params)
    
#%%

# ----------------------------------------------
# -------    EXAMPLE PLOT
# ----------------------------------------------

x = results.groupby(["t", "type"])["x"].mean().reset_index()
y = results.groupby(["t", "type"])["y"].mean().reset_index()
for ty, col in zip([0,1], ["red", "blue"]):
    plt.plot(x.loc[x.type==ty, "x"], y.loc[y.type==ty, "y"], color=col, marker=">", lw=0.5, markersize=2)
    plt.plot(x.loc[(x.t==0) & (x.type==ty), "x"], y.loc[(y.t==0) & (y.type==ty), "y"], color=col, marker="o", markerfacecolor='none')
    plt.plot(x.loc[(x.t==T) & (x.type==ty), "x"], y.loc[(y.t==T) & (y.type==ty), "y"], color=col, marker="x", markersize=10)
plt.ylim(0,1)
plt.xlim(0,1)
plt.gca().set_aspect("equal")
plt.grid()
plt.title(results.attrs.__str__())

# %%
