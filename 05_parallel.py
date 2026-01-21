# %% 
from joblib import Parallel, delayed
import os
import multiprocessing
from si_abm import initialise, update, observe

def run_simulation(params):
    T = 100
    # init
    t = 0
    np.random.seed(params["seed"])
    agents = initialise(params)
    resultcolumns = [
        "t",
        "id",
        "state"
    ]
    results = observe(t, agents)
    for t in range (1,T):
        agents = update(t, agents, params)
        results.extend(observe(t, agents))
    df = pd.DataFrame(results, columns=resultcolumns)
    filename = f"results_r{params['recover_prob']}_i{params['infect_prob']}_{params['seed']}.csv"
    if not os.path.isdir(resultsfolder):
        os.mkdir(resultsfolder)
    df.to_csv(resultsfolder+filename)
    return 

resultsfolder = "results_si_abm/"
params_SensAna = [
      dict(
        n=100,
        infect_prob=i,
        recover_prob=r,
        infected0 = 2,
        link_prob=0.2,
        seed=seed,
    ) for r in [0.05,0.1,0.2] for i in [0.05,0.1,0.2] for seed in range(10)]
Parallel(n_jobs=max(1, multiprocessing.cpu_count() - 2))(
        delayed(run_simulation)(
            params
        )
        for params in params_SensAna
    )
# %%
# STORE AS XARRY DATASET
import xarray as xr
ds_all = []
for params in params_SensAna:
    filename = (
        f"results_r{params['recover_prob']}"
        f"_i{params['infect_prob']}"
        f"_{params['seed']}.csv"
    )
    df = pd.read_csv(resultsfolder+filename, index_col=0)
    ds = xr.Dataset.from_dataframe(
        df.set_index(["t", "id"])
        )
    ds = ds.expand_dims({k: [v] for k, v in params.items()})
    ds_all.append(ds)
ds_all = xr.combine_by_coords(ds_all)
# %%
ds_all
# %%
