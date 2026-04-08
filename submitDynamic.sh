#!/bin/bash
#BSUB -J DynamicParallel100
#BSUB -q hpc
#BSUB -W 10:00
#BSUB -R "rusage[mem=500MB]"
#BSUB -o DynamicParallel100_%J.out
#BSUB -e DynamicParallel100_%J.err
### -- Select specific CPU model --
#BSUB -R "select[model == XeonE5_2650v4]" # run nodestat -F hpc in terminal to see available models 
### -- Set number of cores --
#BSUB -n 24
### -- Set number of nodes/hosts --
#BSUB -R "span[hosts=1]"

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

# Outcomment to check CPU data 
#lscpu

# Run Python script
python SimulateDynamicParallel.py 100
