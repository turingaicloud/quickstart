#!/bin/bash
#SBATCH --output=/mnt/sharefs/home/user6/USERDIR/slurm_log/hello.out
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
export TACC_WORKDIR=/mnt/sharefs/home/user6/WORKDIR/helloworld
export TACC_USERDIR=/mnt/sharefs/home/user6/USERDIR
srun /mnt/sharefs/home/user6/WORKDIR/helloworld/run.sh
