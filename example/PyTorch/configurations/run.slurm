#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
export TACC_WORKDIR=/mnt/sharefs/home/user6/WORKDIR/PyTorch
export TACC_USERDIR=/mnt/sharefs/home/user6/USERDIR
srun /mnt/sharefs/home/user6/WORKDIR/PyTorch/run.sh
