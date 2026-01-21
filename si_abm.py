#%% 
import numpy as np
import pandas as pd

class agent:
    def __init__(self, id, nbs):
        self.id = id
        self.state = 0
        self.nbs = nbs
    

def initialise(params) :
    agents = []
    n = params["n"]
    indices = list(range(n))
    G = np.random.random((n,n)) < params["link_prob"]
    G = np.triu(G) 
    G = G+G.T
    for id in indices:
        ag = agent(id, [j for j in indices if (j!=id) and (G[id,j])])
        agents.append(ag)
    for k in range(params["infected0"]):
        id = np.random.choice(indices)
        ag = agents[id]
        ag.state=1 # initially infected
    return agents

def update(t, agents, params) :
    indices = list(range(len(agents)))
    np.random.shuffle(indices)
    for id in indices:
        ag1 = agents[id]
        ag2 = agents[np.random.choice(ag1.nbs)]
        for sneezer, receiver in [(ag1, ag2), (ag2, ag1)]:
            if sneezer.state==1:
                if np.random.random()< params["infect_prob"]:
                    receiver.state = 1
                if np.random.random() < params["recover_prob"]:
                    sneezer.state=0
    return agents

def observe(t, agents):
    snap = [[t, ag.id, ag.state] for ag in agents]
    return snap

if __name__=="__main__":
    t = 0
    T = 100
    params= dict(
        n=1000,
        infect_prob=0.5,
        recover_prob=0.2,
        infected0 = 2,
        link_prob=10/1000,
        seed=11,
    )
    np.random.seed(params["seed"])
    agents = initialise(params)
    results = observe(t, agents)
    for t in range (1,T):
            agents = update(t, agents, params)
            results.extend(observe(t, agents))
    
    resultColumns = [
        "t",
        "id",
        "state"
    ]
    df = pd.DataFrame(results, columns=resultColumns)

# %%
# df.groupby("t")["state"].sum().plot(x="t")
