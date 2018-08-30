#!/usr/bin/env python3
import subprocess

inraster = "/home/tq/data_pool/Palm/palm_NDVI/maly_NDVI_20.tif"

kalimantan_inshape = "/home/tq/data_pool/Palm/Palm_Shape/kalimantan/kalimantan.shp"
sumatra_inshape = "/home/tq/data_pool/Palm/Palm_Shape/sumatra/sumatra.shp"
malay_inshape = "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp"

clip_kalimantan = "/home/tq/data_pool/Palm/palm_NDVI/maly_NDVI_kalimantan.tif"
clip_sumatra = "/home/tq/data_pool/Palm/palm_NDVI/maly_NDVI_sumatra.tif"
clip_malay = "/home/tq/data_pool/Palm/palm_NDVI/maly_NDVI_malay.tif"

tmp_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        clip_malay,
        "-cutline",
        malay_inshape,
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
if tmp_flag.returncode == 0:
    print("clip aspect dem data sucess.")
else:
    print("clip aspect data failed!")

tmp_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        clip_kalimantan,
        "-cutline",
        kalimantan_inshape,
        "-srcnodata",
        "-3000",
        "-rb",
        "-dstnodata",
        "-3000",
        "-crop_to_cutline",
        "-tr",
        "20",
        "20",
    ]
)
if tmp_flag.returncode == 0:
    print("clip dem data sucess.")
else:
    print("clip data failed!")


tmp_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        clip_sumatra,
        "-cutline",
        sumatra_inshape,
        "-srcnodata",
        "-3000",
        "-dstnodata",
        "-3000",
        "-rb",
        "-crop_to_cutline",
        "-tr",
        "20",
        "20",
    ]
)
if tmp_flag.returncode == 0:
    print("clip slope data sucess.")
else:
    print("clip slope data failed!")
