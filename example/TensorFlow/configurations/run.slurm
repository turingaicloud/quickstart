#!/bin/bash
#SBATCH --nodes=2
export TACC_WORKDIR=/mnt/sharefs/home/testuser/WORKDIR/TensorFlow
export TACC_USERDIR=/mnt/sharefs/home/testuser/USERDIR
srun /mnt/sharefs/home/testuser/WORKDIR/TensorFlow/run.sh
