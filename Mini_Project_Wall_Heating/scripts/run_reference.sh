#!/bin/bash
#BSUB -q hpc
#BSUB -J wall_ref
#BSUB -n 1
#BSUB -W 00:30
#BSUB -R "rusage[mem=2048MB]"

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

cd ~/courses/semester_2/02613_Python_and_Hig_Performance_Computing/Mini_Project_Wall_Heating/src

python time_reference.py 20
