import gdal
import logging
import glob
from pathlib import Path


def change_dtype(tif_name: str) -> bool:
    """
    Funciton
        convert data from db
    Input:
        tif_path
    """

    # check file
    if Path(tif_name).exists():
        logging.info("Will be process %s", tif_name)
    else:
        logging.info("please check %s", tif_name)
        return False

    # open file
    try:
        data_set = gdal.Open(tif_name)
        data = data_set.GetRasterBand(1).ReadAsArray()
    except Exception as e:
        logging.info("%s : %s", tif_name, e)
        return False

    # convert data
    new_data = 10 ** ((data - 10000.0) / 2000.0)

    # creat output
    geotransform = data_set.GetGeoTransform()
    dst_proj = data_set.GetProjection()
    [cols, rows] = data.shape

    # creat output
    try:
        driver = gdal.GetDriverByName("GTiff")
    except Exception:
        print("Creat driver failed!")
        return False

    file_name = tif_name.replace("_clip.tif", ".tif")
    try:
        result_out = driver.Create(file_name, rows, cols, 1, gdal.GDT_Float32)
    except Exception as e:
        print("Creat output failed!", e)
        return False

    result_out.SetGeoTransform(geotransform)
    result_out.SetProjection(dst_proj)
    # result_out.GetRasterBand(1).SetNoDataValue(10000)
    result_out.GetRasterBand(1).WriteArray(new_data)
    result_out.FlushCache()
    result_out = None
    return True


if __name__ == "__main__":
    process_list = glob.glob(
        "/home/tq/data2/X-EX/S1_class_test/cyhq/S1_data/*_clip.tif"
    )
    count = 0
    for tmp in process_list:
        count += 1
        print("processing {} \ {}".format(count, len(process_list)))
        change_dtype(tmp)
