#!/bin/bash
#BSUB -q hpc
#BSUB -J wall_static
#BSUB -n 8
#BSUB -W 01:00
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2048MB]"
#BSUB -R "select[model==XeonGold6142]"
#BSUB -o wall_static_%J.out
#BSUB -e wall_static_%J.err

source /dtu/projects/02613_2025/conda/conda_init.sh
conda activate 02613

cd ~/courses/semester_2/02613_Python_and_High_Performance_Computing/Mini_Project_Wall_Heating

N=100
echo "Running static parallel implementation with N=$N floorplans"

for p in 1 2 4 6 8
do
    echo "----------------------------------------"
    echo "Running with n_workers=$p"
    python src/parallel_static.py $N $p
done