#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --partition=fat_rome
#SBATCH --time=48:00:00

# load python module
module load 2023
module load Python/3.11.3-GCCcore-12.3.0

# activate python virtual environment
source ~/wntr-quantum/.venv/bin/activate

# export environment variables
export EPANET_QUANTUM=~/QuWATER_packages/EPANET
export EPANET_TMP="$TMPDIR"

python Net1.py
