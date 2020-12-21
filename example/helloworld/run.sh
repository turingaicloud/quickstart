#!/bin/bash
source /mnt/sharefs/home/user6/.Miniconda3/etc/profile.d/conda.sh
conda activate hello

python ${TACC_WORKDIR}/main.py \
