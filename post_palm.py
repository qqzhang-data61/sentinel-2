#!/usr/bin/env python3
# import ogr
import subprocess

VH_inraster = "/home/tq/data_pool/Palm/MLY_data/VH/malay_VH_201609.tif"
VV_inraster = "/home/tq/data_pool/Palm/MLY_data/VV/malay_VV_201609.tif"
inshape = "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp"


VV_raster = "/home/tq/data_pool/Palm/MLY_data/VV/MYL_VV_clip.tif"
VH_raster = "/home/tq/data_pool/Palm/MLY_data/VV/MYL_VH_clip.tif"


IDN_flag = subprocess.run(
    [
        "gdalwarp",
        VV_inraster,
        VV_raster,
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

MYS_flag = subprocess.run(
    [
        "gdalwarp",
        VH_inraster,
        VH_raster,
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
if MYS_flag.returncode == 0:
    print("clip data sucess.")
else:
    print("clip data failed!")
