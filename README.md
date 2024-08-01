# Snellius WNTR Quantum scripts and results

Repository containing scripts and results of WNTR quantum experiments in Snellius

## Expected workflow

An example workflow is given for the `Net0` network. The main idea:

1. **Run your simulation and save relevant data**

   To run your `wntr-quantum`, we need to have a `SLURM` script and a python script for your job; see `run_wntr_q.slurm` and `Net0.py` inside `Net0/vqls/`. Then,

   ```console
   sbatch run_wntr_q.slurm
   ```

   After the run is complete, the relevant data, *e.g.*, classical and quantum flows and pressures as well as the network object, should be saved as pickle files.

2. **Load data and make a separate analysis**

   Once all the results are saved, we can perform any analysis we want, without having to repeate any calculation. Note that, before doing anything else, we need to load our object instances from the pickle files, *e.g.*,

   ```python
   with open("quantum_res.pkl", "rb") as f:
    quantum_res = pickle.load(f)
   ```

   An example can be found in the `analysis.py` script inside `Net0/vqls/` that can be run as many times you want as:

   ```console
   python analysis.py
   ```

   Of course, this can be done in your local pc, provided that you push from Snellius the calculated results back to the main repo.

## Installing WNTR Quantum in Snellius

From your home, clone the repo:

```console
git clone git@github.com:QuantumApplicationLab/wntr-quantum.git
```
Here, it might be the case that GitHub asks your credentials; add them as requested. Then,

```console
cd wntr-quantum
```

Before installing the package, we need to create a python virtual environment (avoid using conda in Snellius):

```console
# load python module
module load 2023
module load Python/3.11.3-GCCcore-12.3.0

# create virtual environment
python -m venv .venv
```

Finally, activate the environment and install `wntr-quantum` as usual:

```console
source .venv/bin/activate
pip install -e .
```

Note that you don't need to activate your environment every time you log in to Snellius. This will be done from the `SLURM` submission scripts. You need to do so, however, if you want to perform any analysis of your calculation as discussed above.

## Installing EPANET Quantum in Snellius

As we will be using `wntr-quantum` with `epanet-quantum`, you need also to compile locally this custom EPANET code that can be found at: https://github.com/QuantumApplicationLab/EPANET. 

You can do this with your activated python environment by simply following the instructions given in https://github.com/QuantumApplicationLab/wntr-quantum.

Note that, we don't need to set up the environment variables `EPANET_TMP` and `EPANET_QUANTUM` every time. They will also be set in from `SLURM` submission scripts.
