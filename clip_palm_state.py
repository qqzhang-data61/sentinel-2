#!/usr/bin/env python3
# import ogr
import subprocess

VH_inraster = (
    "/home/tq/data_pool/Palm/MLY_data/sentinel_201709/VH_kalimantan_201709.tif"
)
VV_inraster = (
    "/home/tq/data_pool/Palm/MLY_data/sentinel_201709/VV_kalimantan_201709.tif"
)

inshape = "/home/tq/data_pool/Palm/Palm_Shape/MLY_kalimantan/MLY_kalimantan.shp"


VV_raster = (
    "/home/tq/data_pool/Palm/MLY_data/sentinel_201709/MLY_VV_kalimantan_201709.tif"
)
VH_raster = (
    "/home/tq/data_pool/Palm/MLY_data/sentinel_201709/MLY_VH_kalimantan_201709.tif"
)


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
