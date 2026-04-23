#!/bin/sh 
### General options 
### -- specify queue -- 
#BSUB -q hpc
### -- set the job Name -- 
#BSUB -J miniproject_job6[1-24]
### -- ask for number of cores (default: 1) -- 
#BSUB -n 24
### -- specify that the cores must be on the same host -- 
#BSUB -R "span[hosts=1]"
### -- specify that we need 4GB of memory per core/slot -- 
#BSUB -R "rusage[mem=6GB]"
#BSUB -R "select[model==XeonE5_2650v4]"
### -- set walltime limit: hh:mm -- 
#BSUB -W 180
### -- send notification at start -- 
##BSUB -B 
### -- send notification at completion -- 
##BSUB -N 
### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -o task6_%J_%I.out 
#BSUB -e task6_%J_%I.err 

# here follow the commands you want to execute with input.in as the input file
source /dtu/projects/02613_2025/conda/conda_init.sh

conda activate 02613_2026

export N=100
echo "Running simulation with N=$N floor plans"

time python3 -u simulate_6.py $N $LSB_JOBINDEX