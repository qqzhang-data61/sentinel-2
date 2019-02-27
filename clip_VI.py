#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path
from joblib import Parallel, delayed


def run_clip(inraster, out, shape, nodata: int = -3000, res: int = 20) -> bool:
    """
        clip input by shape
    """
    start_time = time.time()
    print(f"******clip tif {inraster}******\n -> {out}, and using shape {shape}")
    tmp_flag = subprocess.run(
        [
            "gdalwarp",
            inraster,
            out,
            "-cutline",
            shape,
            "-srcnodata",
            str(nodata),
            "-dstnodata",
            str(nodata),
            "-crop_to_cutline",
            "-rc",
            "-tr",
            str(res),
            str(res),
        ]
    )
    end_time = time.time()
    if tmp_flag.returncode == 0:
        print(f"clip {shape}  data sucess, need time {end_time - start_time}")
        return True
    else:
        print(f"clip {shape} failed!")
        return False


def clip_s1(inraster: str):
    """
    function:
        clip S1
    input:
        S1: S1VH_201703.tif
    """
    date_str = Path(inraster).stem.split("_")[1]
    process_flag = Path(inraster).stem.split("_")[0]
    shape_list = [
        "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/MLY_kalimantan/MLY_SBH.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/MLY_kalimantan/MLY_SRW.shp",
    ]
    # suffix = ["_SBH_", "_SRW_"]
    suffix = ["_malay_", "_SBH_", "_SRW_"]
    out_list = [
        Path(inraster).with_name(process_flag + name + date_str + ".tif")
        for name in suffix
    ]

    Parallel(n_jobs=2)(
        delayed(run_clip)(inraster, out, shape)
        for out, shape in zip(out_list, shape_list)
    )


if __name__ == "__main__":
    file_name = "/home/tq/data_pool/Palm/palm_NDVI/201609/NDVI_201609.tif"
    clip_s1(file_name)
