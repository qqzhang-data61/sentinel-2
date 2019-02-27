#!/usr/bin/env python3
import subprocess


# inraster = "/home/tq/data_pool/china_crop/s1_rice_test/clip_tif/VH_all.img"
inraster = "/home/tq/data_pool/Eric/heishan_s1_data/Overall/VV_med3.tif"
inshape = "/home/tq/data_pool/china_crop/vector/heishan_xiangzhen_1.shp"


result = "/home/tq/data_pool/Eric/heishan_s1_data/Overall/VV_med3_cliped.tif"

tmp_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        result,
        "-cutline",
        inshape,
        "-srcnodata",
        "10000",
        "-dstnodata",
        "10000",
        "-rb",
        "-overwrite",
        "-crop_to_cutline",
    ]
)
if tmp_flag.returncode == 0:
    print("clip dem data sucess.")
else:
    print("clip data failed!")
