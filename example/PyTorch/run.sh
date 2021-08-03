#!/bin/bash
source /mnt/home/coco/.Miniconda3/etc/profile.d/conda.sh
conda activate 755c9df7b9e3837d5eb7d80ee6bab896

VISIBLE_CUDA_DEVICES='0' GLOO_SOCKET_IFNAME=eno1 python ${TACC_WORKDIR}/mnist.py --epoch=3 \
