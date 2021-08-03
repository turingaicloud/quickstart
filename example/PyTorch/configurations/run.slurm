#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
export TACC_WORKDIR=/mnt/home/coco/WORKDIR/PyTorch
export TACC_USERDIR=/mnt/home/coco/USERDIR
srun /mnt/home/coco/WORKDIR/PyTorch/run.sh
