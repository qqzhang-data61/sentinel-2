#!/usr/bin/env python3
import re
import pprint

from pathlib import Path
from pyhdf.SD import SD
from osgeo import osr
from osgeo import gdal

pp = pprint.PrettyPrinter()


def get_value(t: str, str_flag: str) -> float:
    tmp_str = t[0].split(str_flag)[1].split("=")[2]
    return float(re.findall(r"\d+\.?\d*", tmp_str)[0])


def convet_modis_tif(file_name: str) -> str:
    """
        get the modis ndvi and evi to convert tif
    """
    # open the hdf file
    try:
        hdf = SD(file_name)
    except Exception as e:
        print(e)

    # get ndvi and evi data
    NDVI_obj = hdf.select("250m 16 days NDVI")
    NDVI = NDVI_obj[:]

    EVI_obj = hdf.select("250m 16 days EVI")
    EVI = EVI_obj[:]

    attr = hdf.attributes(full=1)
    t = attr["ArchiveMetadata.0"]

    # get the GeoTransform [lon, x_res, 0, lat, 0, -y_res]
    tmp = []
    for tmp_str in [
        "NORTHBOUNDINGCOORDINATE",
        "WESTBOUNDINGCOORDINATE",
        "CHARACTERISTICBINSIZE",
    ]:
        tmp.append(get_value(t, tmp_str))
    GeoTransform = [tmp[1], tmp[2], 0, tmp[0], 0, -tmp[2]]

    # set Spatial Reference
    proj = osr.SpatialReference()
    proj.ImportFromEPSG(4326)
    proj.ExportToWkt()

    result_file = Path(file_name).with_name("DNVI.tif")
    write_img(result_file, proj, GeoTransform, NDVI)


def write_img(filename, im_proj, im_geotrans, im_data):
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64

    # 判断栅格数据的数据类型
    if "int8" in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif "int16" in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # 判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    # 创建文件
    driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(im_proj)  # 写入投影

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])

    del dataset


if __name__ == "__main__":
    file_name = "/home/tq/data_pool/Palm/palm_NDVI/201703/HDF/MOD13Q1.A2017081.h27v08.006.2017111085102.hdf"
    convet_modis_tif(file_name)
