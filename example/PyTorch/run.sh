#!/bin/bash
source /mnt/sharefs/home/user6/.Miniconda3/etc/profile.d/conda.sh
conda activate torch-env

VISIBLE_CUDA_DEVICES='0' GLOO_SOCKET_IFNAME=enp1s0f1 python ${TACC_WORKDIR}/mnist.py --epoch=3 \
