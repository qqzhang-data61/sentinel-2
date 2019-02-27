import zipfile
import json
import os
import pprint
from osgeo import ogr
from osgeo import osr
import re

printer = pprint.PrettyPrinter()
home_dir = os.path.expanduser("~")


def create_shp_fromZip(json_path, res_name):
    # Get zip filelist
    with open(json_path) as json_file:
        zipFileList = json.load(json_file)
    zipFileList = [os.path.join(home_dir, zipFile) for zipFile in zipFileList]
    printer.pprint(zipFileList)

    # Set shapefile param
    driver = ogr.GetDriverByName("ESRI Shapefile")
    data_source = driver.CreateDataSource(res_name)
    # Create name field
    srs = osr.SpatialReference()
    # srs.SetProjection()
    srs.ImportFromEPSG(4326)
    layer = data_source.CreateLayer("polygon", srs, ogr.wkbPolygon)
    field_name = ogr.FieldDefn("name", ogr.OFTString)
    field_name.SetWidth(100)
    layer.CreateField(field_name, 1)

    for zipFileName in zipFileList:
        # Get kml file
        try:
            azip = zipfile.ZipFile(zipFileName)
            kmlFile = azip.read(
                os.path.join(
                    os.path.basename(zipFileName).replace(".zip", ".SAFE"),
                    "preview/map-overlay.kml",
                )
            ).decode("utf-8")
        except Exception as e:
            printer.pprint(e)

        # Find coordinates from kml file
        coor_index = [coor.start() for coor in re.finditer("coordinates", kmlFile)]
        coor_strs = (kmlFile[coor_index[0] + 12 : coor_index[1] - 2]).split(" ")
        print(coor_strs)
        coor_lats = [float(coor_str.split(",")[0]) for coor_str in coor_strs]
        coor_lons = [float(coor_str.split(",")[1]) for coor_str in coor_strs]

        # Create shp feature
        feature = ogr.Feature(layer.GetLayerDefn())
        keyname = zipFileName
        print("key:", keyname)
        feature.SetField(0, keyname)

        ring = ogr.Geometry(ogr.wkbLinearRing)
        for index in range(5):
            ring.AddPoint(coor_lats[index % 4], coor_lons[index % 4])
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        feature.SetGeometry(poly)
        layer.CreateFeature(feature)
        feature = None

    data_source.Destroy()
    return True


if __name__ == "__main__":
    json_path = "/home/tq/data2/citrus/sichuan_S1/sichuan_S1.json"
    res_name = "/home/tq/data2/citrus/sichuan_S1/sichuan_S1.shp"
    status = create_shp_fromZip(json_path, res_name)
    if status:
        print("create shape file success!")
    else:
        print("create shape file failed!")
