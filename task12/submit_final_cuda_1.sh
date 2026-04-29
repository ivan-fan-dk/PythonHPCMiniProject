#!/bin/bash
#BSUB -J final_1_new
#BSUB -q c02613
#BSUB -W 00:30
#BSUB -R "rusage[mem=5GB]"
#BSUB -o final_1_new_%J.out
#BSUB -e final_1_new_%J.err
### -- Set number of cores (max 4 for GPU at c02613 queue) --
#BSUB -n 4
### -- Set number of nodes/hosts --
#BSUB -R "span[hosts=1]"
#BSUB -gpu "num=1:mode=exclusive_process"

# Initialize Python environment
source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613_2026 # change to 02613_2026 for update

# Outcomment to check CPU data 
#lscpu

# Run Python script
python jacobi_cuda_final.py 0 1000