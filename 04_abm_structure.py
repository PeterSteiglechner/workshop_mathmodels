# imports


# agent
class agent:
    pass


# Functiopns
def initialise(params):
    agents = []
    # ...
    return agents


def update(t, agents, params):
    # ...
    return agents


def observe(t, agents):
    snap = []
    # ... plot / store the results
    return snap


# Main
if __name__ == "__main__":
    t = 0
    T = 100
    params = dict(a=1, b=2, seed=2026)
    np.random.seed(params["seed"])
    # Main Loop
    agents = initialise(params)
    results = observe(t, agents)
    for t in range(1, T):
        agents = update(t, agents, params)
        results.extend(observe(t, agents))
