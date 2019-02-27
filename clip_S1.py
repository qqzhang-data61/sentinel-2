#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path
from joblib import Parallel, delayed


def run_clip(inraster, out, shape, nodata: int = 0, res: int = 20) -> bool:
    """
        clip input by shape
    """
    start_time = time.time()
    if "NDVI" in inraster or "EVI" in inraster:
        nodata = -3000
    elif "dem" in inraster:
        nodata = -32768
    else:
        nodata = 0
    print(f"clip tif {inraster}\n -> {out}, and using shape {shape}")
    print(f"nodata use value {nodata}")
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
    date_str = Path(inraster).stem.split("_")[-1]
    process_flag = Path(inraster).stem.split("_")[0]
    shape_list = [
        # "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/MLY_kalimantan/MLY_SBH.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/MLY_kalimantan/MLY_SRW.shp",
    ]
    # suffix = ["_MLY_", "_SBH_", "_SRW_"]
    suffix = ["_SBH_", "_SRW_"]

    # shape_list = [
    #     "/home/tq/data_pool/Palm/Palm_Shape/malay/test_state/KL.shp",
    #     "/home/tq/data_pool/Palm/Palm_Shape/malay/test_state/KP.shp",
    # ]

    # suffix = ["_MLY_KL_", "_MLY_KP_"]

    out_list = [
        Path(inraster).with_name(process_flag + name + date_str + ".tif")
        for name in suffix
    ]

    Parallel(n_jobs=len(suffix))(
        delayed(run_clip)(inraster, out, shape)
        for out, shape in zip(out_list, shape_list)
    )


if __name__ == "__main__":
    file_name2 = (
        "/home/tq/data_pool/Palm/MLY_data/sentinel_201609/Kalimantan/S1VV_201609.tif"
    )
    clip_s1(file_name2)
