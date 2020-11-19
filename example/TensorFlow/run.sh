#!/bin/bash
source /mnt/sharefs/home/testuser/WORKDIR/miniconda3/etc/profile.d/conda.sh
conda activate tf

python ${TACC_WORKDIR}/mnist.py \
--task_index=0 \
--data_dir=${TACC_WORKDIR}/datasets/mnist_data \
--batch_size=1 \
