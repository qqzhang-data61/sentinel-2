import glob
import os

glob_path = "/home/tq/tq-data05/sentinel1_DB/62_P/*_IW_GRDH_1SDV*"
cutline = "/home/tq/data2/citrus/pujiang/shape/pujiang_rep.shp"
result_root = "/home/tq/data2/citrus/pujiang/S1"
path_list = glob.glob(glob_path)
prj_file = "/home/tq/data_pool/Ray_EX/PRJ_FILE/china_wgs84.prj"
ps = 20

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
    cmd_str = "gdalwarp -t_srs {} -r cubic -tr {} {} {} {}".format(
        prj_file, ps, ps, process_vv, result_vv
    )
    print(cmd_str)
    os.system(cmd_str)

    # this for vh
    cmd_str = "gdalwarp -t_srs {} -r cubic -tr {} {} {} {}".format(
        prj_file, ps, ps, process_vh, result_vh
    )
    print(cmd_str)
    os.system(cmd_str)


def s1_rep_clip(work_dir, shape_file, ps=20):
    merger_list = glob.glob(os.path.join(work_dir, "*_rep.tif"))
    for tmp_file in merger_list:
        result_tmp = tmp_file.replace(".tif", "_clip.tif")
        cmd_str = "gdalwarp -r cubic  -tr 20 20 -cutline {} -crop_to_cutline {} {}".format(
            shape_file, tmp_file, result_tmp
        )
        os.system(cmd_str)

if __name__ == "__main__":

