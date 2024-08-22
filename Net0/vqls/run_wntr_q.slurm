#!/bin/bash
#SBATCH --partition=fat_rome
#SBATCH --time=0:30:00

# load python module
module load 2023
module load Python/3.11.3-GCCcore-12.3.0

# activate python virtual environment
source ~/wntr-quantum/.venv/bin/activate

# export environment variables
export EPANET_QUANTUM=~/QuWATER_packages/EPANET
export EPANET_TMP="$TMPDIR"

python Net0.py
