#!/bin/bash
#BSUB -J jacobiCuPy_nsys
#BSUB -q c02613
#BSUB -W 00:30
#BSUB -R "rusage[mem=5GB]"
#BSUB -o jacobiCuPy_nsys_%J.out
#BSUB -e jacobiCuPy_nsys_%J.err
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
python jacobi_cupy.py 20

# Outcomment for profiling
#module swap cuda cuda/13.2.0
#nsys profile -o cupy_prof python jacobi_cupy.py 20