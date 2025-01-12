import os.path as osp
from glob import glob
import argparse
import ast

from loguru import logger
from soma.amass.mosh_manual import mosh_manual

parser = argparse.ArgumentParser(description="Mosh++ runner", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("-m", "--mocap_base_dir", help="Path to the directory containing motion capture data. It is assumed that subdirectories for individual subjects exist directly under this directory, with `.c3d` files located within those subdirectories.", default="~/MOSHPP_WORK_BASE/support_files/evaluation_mocaps/original/SOMA_manual_labeled")
parser.add_argument("-w", "--work_base_dir", help="Path to the directory where results from Mosh++ will be saved.", default="~/MOSHPP_WORK_BASE/running_just_mosh")

parser.add_argument("--support_base_dir", help="Path to the directory containing `support_files` required for running Mosh++.", default="~/MOSHPP_WORK_BASE/support_files")
parser.add_argument("--max_num_jobs", type=int, help="Number of `.c3d` files to process with Mosh++.", default=1)
parser.add_argument("--subject", help="Specify a single subject to process if you want to limit execution to one specific individual.", default="")
parser.add_argument("--rotation", help="Specify [x, y, z] rotation angles in degrees to adjust the orientation if needed. The motion capture data assumes the z-axis is up.", default="[0,0,0]")
parser.add_argument("--unit", choices=["mm", "cm", "m"], help="Specify the unit of measurement if the `.c3d` files are not in millimeters.", default="mm")
parser.add_argument("--cpu_count", type=int, help="Number of CPUs to use for parallel processing.", default=256)

args = parser.parse_args()

def main(args):
    support_base_dir = osp.expanduser(args.support_base_dir)
    mocap_base_dir = osp.expanduser(args.mocap_base_dir)
    work_base_dir = osp.expanduser(args.work_base_dir)

    if args.subject:
        mocap_fnames = glob(osp.join(mocap_base_dir,  f"{args.subject}/*.c3d"))
    else:
        mocap_fnames = glob(osp.join(mocap_base_dir,  "*/*.c3d"))

    logger.info(f"#mocaps found for {mocap_base_dir}: {len(mocap_fnames)}")

    rotation = ast.literal_eval(args.rotation)
    cpu_count = args.cpu_count
    max_num_jobs = args.max_num_jobs

    mosh_manual(
        mocap_fnames,
        mosh_cfg={
            "moshpp.verbosity": 1, # set to 2 to visulaize the process in meshviewer
            "mocap.rotate": rotation,
            "mocap.unit": args.unit,
            "dirs.work_base_dir": osp.join(work_base_dir, "mosh_results"),
            "dirs.support_base_dir": support_base_dir,
        },
        render_cfg={
            "dirs.work_base_dir": osp.join(work_base_dir, "mp4_renders"),
            "render.render_engine": "eevee",  # eevee / cycles,
            # "render.render_engine": "cycles",  # eevee / cycles,
            "render.show_markers": True,
            # "render.save_final_blend_file": True
            "dirs.support_base_dir": support_base_dir,
        },
        parallel_cfg={
            "pool_size": 1,
            "max_num_jobs": max_num_jobs,
            "randomly_run_jobs": True,
            "gpu_memory": 0,
            "cpu_count": cpu_count,
            "gpu_count": 0,
        },
        run_tasks=[
            "mosh",
            # "render",
        ],
        # fast_dev_run=True,
    )


if __name__ == "__main__":
    main(args)