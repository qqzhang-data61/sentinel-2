#!/usr/bin/env python3
import subprocess

inraster = "/tmp/palm_201712/S1_VV_201712.tif"

kalimantan_inshape = "/home/tq/data_pool/Palm/Palm_Shape/kalimantan/kalimantan.shp"
sumatra_inshape = "/home/tq/data_pool/Palm/Palm_Shape/sumatra/sumatra.shp"
malay_inshape = "/home/tq/data_pool/Palm/Palm_Shape/peninsula_Shp/MYS_adm1.shp"

clip_kalimantan = "/tmp/palm_201712/VV_kalimantan_201712.tif"
clip_sumatra = "/tmp/palm_201712/VV_sumatra_201712.tif"
clip_malay = "/tmp/palm_201712/VV_malay_201712.tif"

# tmp_flag = subprocess.run(
#     [
#         "gdalwarp",
#         inraster,
#         clip_malay,
#         "-cutline",
#         malay_inshape,
#         "-srcnodata",
#         "0",
#         "-dstnodata",
#         "0",
#         "-crop_to_cutline",
#         "-rc",
#         "-tr",
#         "20",
#         "20",
#     ]
# )
# if tmp_flag.returncode == 0:
#     print("clip malay VV data sucess.")
# else:
#     print("clip malay VV data failed!")


# tmp_flag = subprocess.run(
#     [
#         "gdalwarp",
#         inraster,
#         clip_kalimantan,
#         "-cutline",
#         kalimantan_inshape,
#         "-srcnodata",
#         "0",
#         "-rc",
#         "-dstnodata",
#         "0",
#         "-crop_to_cutline",
#         "-tr",
#         "20",
#         "20",
#     ]
# )
# if tmp_flag.returncode == 0:
#     print("clip kalimantan VV data sucess.")
# else:
#     print("clip kalimantan VV failed!")


tmp_flag = subprocess.run(
    [
        "gdalwarp",
        inraster,
        clip_sumatra,
        "-cutline",
        sumatra_inshape,
        "-srcnodata",
        "0",
        "-dstnodata",
        "0",
        "-rc",
        "-crop_to_cutline",
        "-tr",
        "20",
        "20",
    ]
)
if tmp_flag.returncode == 0:
    print("clip sumatra VV  data sucess.")
else:
    print("clip sumatra VV data failed!")
