#!/usr/bin/env python3
# import ogr
import subprocess

inraster = "/home/tq/data_pool/Palm/shape/malaysia_ground_truth/new_label/all_label.tif"
inshape = "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp"

raster = (
    "/home/tq/data_pool/Palm/shape/malaysia_ground_truth/new_label/all_label_clip.tif"
)

IDN_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        raster,
        "-cutline",
        inshape,
        "-crop_to_cutline",
        "-srcnodata",
        "0",
        "-dstnodata",
        "0",
        "-rc",
        "-tr",
        "20",
        "20",
    ]
)
if IDN_flag.returncode == 0:
    print("clip data sucess.")
else:
    print("clip data failed!")
