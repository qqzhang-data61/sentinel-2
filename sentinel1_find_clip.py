import glob
import os
import subprocess

glob_path = "/home/tq/tq-data05/sentinel1_DB/69/*_IW_GRDH_1SDV_201804*"
cutline = "/home/tq/data_pool/china_crop/tianchang/shape/tianchang.shp"
result_root = "/home/tq/data_pool/china_crop/tianchang/S1_rep_clip/rep"
path_list = glob.glob(glob_path)


count = 0

for path in path_list:
    count += 1
    print("total %d: now process %d" % (len(path_list), count))

    # now process VV
    process_vv = glob.glob(os.path.join(path, "*VV.tif"))[0]
    tif_name = os.path.split(process_vv)[-1].replace(".tif", "_rep.tif")
    result_vv = os.path.join(result_root, tif_name)

    process_vh = glob.glob(os.path.join(path, "*VH.tif"))[0]
    tif_name = os.path.split(process_vh)[-1].replace(".tif", "_rep.tif")
    result_vh = os.path.join(result_root, tif_name)

    # this for vv
    tmp_flag = subprocess.run(
        [
            "gdalwarp",
            process_vv,
            result_vv,
            "-t_srs",
            "/home/tq/data_pool/Ray_EX/PRJ_FILE/china_wgs84.prj",
            "-cutline",
            cutline,
            "-rc",
            "-overwrite",
            "-crop_to_cutline",
        ]
    )
    if tmp_flag.returncode == 0:
        print("clip %s vv data sucess." % path)
    else:
        print("clip %s vv data failed!" % path)

    # this for vh
    tmp_flag = subprocess.run(
        [
            "gdalwarp",
            process_vh,
            result_vh,
            "-cutline",
            cutline,
            "-rc",
            "-overwrite",
            "-crop_to_cutline",
        ]
    )
    if tmp_flag.returncode == 0:
        print("clip %s vh data sucess." % path)
    else:
        print("clip %s vh data failed!" % path)
