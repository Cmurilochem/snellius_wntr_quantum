# Snellius WNTR Quantum scripts and results

Repository containing scripts and results of WNTR quantum experiments in Snellius

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

Note that you don't need to activate your environment every time you log in to Snellius. This will be done from the `SLURM` submission scripts.

### Installing EPANET Quantum in Snellius

As we will be using `wntr-quantum` with `epanet-quantum`, you need also to compile locally this custom EPANET code that can be found at: https://github.com/QuantumApplicationLab/EPANET. To install it, simply follow the instructions given in https://github.com/QuantumApplicationLab/wntr-quantum.

Note that, we don't need to set up the environment variables `EPANET_TMP` and `EPANET_QUANTUM` every time. They will also be set in the `SLURM` submission scripts.
