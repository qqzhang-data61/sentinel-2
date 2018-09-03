#!/usr/bin/env python3
import subprocess
import time
from pathlib import Path


def clip_modis(inraster: str):
    date_str = Path(inraster).stem.split("_")[1]
    process_flag = Path(inraster).stem.split("_")[0]
    shape_list = [
        "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/sumatra/sumatra.shp",
        "/home/tq/data_pool/Palm/Palm_Shape/kalimantan/kalimantan.shp",
    ]
    # suffix = ["_sumatra_", "_kalimantan_"]
    suffix = ["_malay_", "_sumatra_", "_kalimantan_"]
    out_list = [
        Path(inraster).with_name(process_flag + name + date_str + ".tif")
        for name in suffix
    ]
    for out, shape in zip(out_list, shape_list):
        start_time = time.time()
        print(f"clip tif -> {out}, and using shape {shape}")
        tmp_flag = subprocess.run(
            [
                "gdalwarp",
                inraster,
                out,
                "-cutline",
                shape,
                "-srcnodata",
                "-3000",
                "-dstnodata",
                "-3000",
                "-crop_to_cutline",
                "-rb",
                "-tr",
                "20",
                "20",
            ]
        )
        end_time = time.time()
        if tmp_flag.returncode == 0:
            print(f"clip {shape} VI data sucess, need time {end_time - start_time}")
        else:
            print(f"clip {shape} VI failed!")
        print()


if __name__ == "__main__":
    file_name = "/home/tq/data_pool/Palm/palm_NDVI/201706/EVI_201706.tif"
    clip_modis(file_name)
