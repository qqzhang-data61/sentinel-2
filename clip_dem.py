#!/usr/bin/env python3
import subprocess

dem_inraster = "/home/tq/data_pool/Palm/palm_dem/malay/maly_dem_20_cubic.tif"
slope_inraster = "/home/tq/data_pool/Palm/palm_dem/malay/maly_dem_slope.tif"
aspect_inraster = "/home/tq/data_pool/Palm/palm_dem/malay/maly_dem_aspect.tif"
inshape = "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp"


clip_dem = "/home/tq/data_pool/Palm/palm_dem/maly_dem_clip.tif"
clip_slope = "/home/tq/data_pool/Palm/palm_dem/maly_dem_slope_clip.tif"
clip_aspect = "/home/tq/data_pool/Palm/palm_dem/maly_dem_aspect_clip.tif"

tmp_flag = subprocess.run(
    [
        "gdalwarp",
        dem_inraster,
        clip_dem,
        "-cutline",
        inshape,
        "-srcnodata",
        "-32768",
        "-rb",
        "-dstnodata",
        "-32768",
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
        slope_inraster,
        clip_slope,
        "-cutline",
        inshape,
        "-srcnodata",
        "-1",
        "-dstnodata",
        "-1",
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

tmp_flag = subprocess.run(
    [
        "gdalwarp",
        aspect_inraster,
        clip_aspect,
        "-cutline",
        inshape,
        "-srcnodata",
        "-1",
        "-dstnodata",
        "-1",
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
