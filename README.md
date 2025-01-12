# Mosh++ runner
This is a docker container to make running [Mosh++](https://github.com/nghorbani/moshpp) easier!


## Download dependencies
Download all of the following dependent files and place them in `/downloads`. 

- [bpy-2.83](https://download.is.tue.mpg.de/download.php?domain=soma&sfile=blender/bpy-2.83-20200908.tar.bz2)
- [smpl-fast-derivative](https://download.is.tue.mpg.de/download.php?domain=soma&sfile=smpl-fast-derivatives.tar.bz2)
- [pretrained SOMA model for the SOMA dataset](https://download.is.tue.mpg.de/download.php?domain=soma&sfile=training_experiments/V48_02_SOMA.tar.bz2)
- [SMPL-X locked head body model](https://download.is.tue.mpg.de/download.php?domain=smplx&sfile=smplx_locked_head.tar.bz2)
- [extra smplx data](https://download.is.tue.mpg.de/download.php?domain=soma&sfile=smplx/extra_smplx_data.tar.bz2)
- [SSM head marker covariances](https://download.is.tue.mpg.de/soma/ssm_head_marker_corr.npz)
- [SOMA dataset's manually labeled mocaps](https://download.is.tue.mpg.de/download.php?domain=soma&sfile=evaluation_mocaps/original/SOMA_dataset/SOMA_manual_labeled.tar.bz2) (Optional)


## Run Mosh++
### create docker image
```bash
$ docker build -f ./docker/Dockerfile -t moshpp-runner .
$ docker run --privileged -it moshpp-runner bash
```

### inside container
```bash
$ bash setup.sh
$ python run_moshpp.py
```

### run_moshpp.py
| option | description | default |
| --- | --- | --- |
| `--mocap_base_dir`, `-m` | Path to the directory containing motion capture data. It is assumed that subdirectories for individual subjects exist directly under this directory, with `.c3d` files located within those subdirectories. | `"~/MOSHPP_WORK_BASE/support_filesevaluation_mocaps/original/SOMA_manual_labeled"` |
| `--work_base_dir`, `-w` | Path to the directory where results from Mosh++ will be saved. | `"~/MOSHPP_WORK_BASE/running_just_mosh"` |
| `--support_base_dir` | Path to the directory containing `support_files` required for running Mosh++. | `"~/MOSHPP_WORK_BASE/support_files"` |
| `--max_num_jobs` | Number of `.c3d` files to process with Mosh++. | `1` |
| `--subject` | Specify a single subject to process if you want to limit execution to one specific individual. | `""` |
| `--rotation` | Specify [x, y, z] rotation angles in degrees to adjust the orientation if needed. The motion capture data assumes the z-axis is up. | `"[0,0,0]"` |
| `--unit` | Specify the unit of measurement if the `.c3d` files are not in millimeters. `"mm"`, `"cm"` `"m"` | `"mm"` |
| `--cpu_count` | Number of CPUs to use for parallel processing. | 256 |