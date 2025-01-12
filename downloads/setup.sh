#!/bin/bash

SITE_PACKAGES="$HOME/miniconda3/envs/moshpp/lib/python3.7/site-packages/"
WORK_BASE_DIR="$HOME/MOSHPP_WORK_BASE"


tar -jxvf smpl-fast-derivatives.tar.bz2
mv psbody/smpl "$SITE_PACKAGES/psbody_mesh-0.4-py3.7-linux-x86_64.egg/psbody/."
rm -f smpl-fast-derivatives.tar.bz2

tar -jxvf bpy-2.83-20200908.tar.bz2 -C "$SITE_PACKAGES"
rm -f bpy-2.83-20200908.tar.bz2


mkdir -p "$WORK_BASE_DIR/training_experiments"
mkdir -p "$WORK_BASE_DIR/support_files/smplx"
mkdir -p "$WORK_BASE_DIR/support_files/evaluation_mocaps"

tar -jxvf V48_02_SOMA.tar.bz2 -C "$WORK_BASE_DIR/training_experiments"
rm -f V48_02_SOMA.tar.bz2

tar -jxvf smplx_locked_head.tar.bz2 -C "$WORK_BASE_DIR/support_files/smplx"
rm -f smplx_locked_head.tar.bz2

tar -jxvf extra_smplx_data.tar.bz2 -C "$WORK_BASE_DIR/support_files/smplx"
rm -f extra_smplx_data.tar.bz2

mv ssm_head_marker_corr.npz "$WORK_BASE_DIR/support_files/."

if [ -e "SOMA_manual_labeled.tar.bz2" ]; then
    mkdir -p "$WORK_BASE_DIR/support_files/evaluation_mocaps/original"
    tar -jxvf SOMA_manual_labeled.tar.bz2 -C "$WORK_BASE_DIR/support_files/evaluation_mocaps/original"
    rm -f SOMA_manual_labeled.tar.bz2
fi