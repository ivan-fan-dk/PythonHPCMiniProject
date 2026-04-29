#!/bin/sh 
### General options 
### -- specify queue -- 
#BSUB -q c02613
### -- set the job Name -- 
#BSUB -J miniproject_job10
### -- ask for number of cores (default: 1) -- 
#BSUB -n 8
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 4GB of memory per core/slot -- 
#BSUB -R "rusage[mem=5GB]"
### -- set walltime limit: hh:mm -- 
#BSUB -W 25
### -- send notification at start -- 
#BSUB -B 
### -- send notification at completion -- 
#BSUB -N 
### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -o task10.out 
#BSUB -e task10.err 

# here follow the commands you want to execute with input.in as the input file
source /dtu/projects/02613_2025/conda/conda_init.sh

conda activate 02613_2026

export N=20
echo "Running simulation with N=$N floor plans"

time python -u simulate_9.py $N
module swap cuda cuda/13.2.0
nsys profile -o task10_prof python simulate_9.py $N