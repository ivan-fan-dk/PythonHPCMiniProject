#!/bin/sh 
### General options 
### -- specify queue -- 
#BSUB -q hpc
### -- set the job Name -- 
#BSUB -J miniproject_job
### -- ask for number of cores (default: 1) -- 
#BSUB -n 4
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 4GB of memory per core/slot -- 
#BSUB -R "rusage[mem=5GB]"
#BSUB -R "select[model==XeonGold6126]"
### -- set walltime limit: hh:mm -- 
#BSUB -W 60
### -- send notification at start -- 
#BSUB -B 
### -- send notification at completion -- 
#BSUB -N 
### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -o task5r.out 
#BSUB -e task5r.err 

# here follow the commands you want to execute with input.in as the input file
source /dtu/projects/02613_2025/conda/conda_init.sh

conda activate 02613

export N=24
echo "Running simulation with N=$N floor plans"

for num_workers in 1 2 3 4 6 8 12 18 24
do
    time python3 -u simulate_5.py $N $num_workers
done