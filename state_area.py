import warnings
import numpy as np
from osgeo import gdal, gdalnumeric, ogr
import os
from PIL import Image, ImageDraw
import settings
import cv2

warnings.filterwarnings("ignore")


def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    a = gdalnumeric.fromstring(i.tobytes(), "b")
    a.shape = i.im.size[1], i.im.size[0]
    return a


def arrayToImage(a):
    """
    Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    i = Image.frombytes("L", (a.shape[1], a.shape[0]), (a.astype("b")).tobytes())
    return i


def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    pixel = int((x - ulX) / xDist)
    line = int((ulY - y) / xDist)
    return (pixel, line)


def data_shuffle(data):
    idx = np.arange(len(data))
    np.random.shuffle(idx)
    data = data[idx, :]
    return data


def get_area_by_state(palmmask, geoTrans, stateshppath, yearlabel):
    shapef = ogr.Open(stateshppath)
    lyr = shapef.GetLayer()
    arealist = []  # list which store area infos
    # arealist.append(["Name", "MPOB_area", "palm_area", "Error"])
    npoly = 0
    poly = lyr.GetNextFeature()
    while poly:
        # loop poly in lyr
        # Convert the layer extent to image pixel coordinates
        if npoly > 11:
            break
        pid = poly.GetField("NAME_1")
        npoly = npoly + 1
        # print(npoly, pid)
        geon = poly.GetGeometryRef()
        geontype = geon.GetGeometryType()
        if geon.GetGeometryType() not in [3, 6]:
            raise SystemExit("This module can only load polygon/multipolygons")
        minX, maxX, minY, maxY = geon.GetEnvelope()
        ulX, ulY = world2Pixel(geoTrans, minX, maxY)
        lrX, lrY = world2Pixel(geoTrans, maxX, minY)
        # Calculate the pixel size of the new image
        pxWidth = int(lrX - ulX)
        pxHeight = int(lrY - ulY)
        clip = palmmask[ulY:lrY, ulX:lrX]

        # Create a new geomatrix for the image
        ngeoTrans = list(geoTrans)
        ngeoTrans[0] = minX
        ngeoTrans[3] = maxY

        # Map points to pixels
        points = []
        pixels = []

        # for multipolygons
        geontype = geon.GetGeometryType()
        if geontype == 6:
            # multipolygon
            rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
            rasterize = ImageDraw.Draw(rasterPoly)
            i = 0

            for geonpart in geon:
                # loop each part polygon
                i = i + 1
                pts = geonpart.GetGeometryRef(0)
                np = pts.GetPointCount()
                points = []
                pixels = []
                if np == 0:
                    continue
                for p in range(pts.GetPointCount()):
                    points.append((pts.GetX(p), pts.GetY(p)))
                for p in points:
                    pixels.append(world2Pixel(ngeoTrans, p[0], p[1]))
                rasterize.polygon(pixels, 0)
            mask = imageToArray(rasterPoly)

        # for polygons
        if geon.GetGeometryType() == 3:
            points = []
            pixels = []
            rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
            rasterize = ImageDraw.Draw(rasterPoly)
            pts = geon.GetGeometryRef(0)
            for p in range(pts.GetPointCount()):
                points.append((pts.GetX(p), pts.GetY(p)))
            for p in points:
                pixels.append(world2Pixel(ngeoTrans, p[0], p[1]))
            rasterPoly = Image.new("L", (pxWidth, pxHeight), 1)
            rasterize = ImageDraw.Draw(rasterPoly)
            rasterize.polygon(pixels, 0)
            mask = imageToArray(rasterPoly)

        # Clip the image using the mask and calculate palm percentage
        cliped = gdalnumeric.choose(mask, (clip, 0))  # .astype(gdalnumeric.uint8)
        x = cliped[cliped > 0]  # watch out >0
        palmnum = len(x)
        palm_area = round(palmnum * 20 * 20 * 0.0001, 2)
        MPOB_area = settings.MPOB_data[yearlabel][pid]
        palm_error = round(100.0 * (palm_area - MPOB_area) / (MPOB_area), 2)
        arealist.append([pid, MPOB_area, palm_area, palm_error])
        poly = lyr.GetNextFeature()
    return arealist


if __name__ == "__main__":
    homedir = os.path.expanduser("~")
    locateLabel = "peninsula"
    shapefile_path = homedir + "/data_pool/zgq/vector/malay.shp"

    mask_path = homedir + "/tq-data05/Palm_test/peninsula data/mix_mask.tif"

    DEM_mask_path = settings.raster_path[locateLabel]["DEM"]
    EVI_mask_path = settings.raster_path[locateLabel]["201609"]["EVI"]
    qipa_mask_path = settings.mask_raster_path[locateLabel]

    fileName = homedir + "/tq-data05/Palm_test/peninsula data/mix_res.tif"

    palm_file_path = {
        "201609": homedir
        + "/data_pool/Palm/MLY_data/DT_Res/post_mask_index_201609.tif",
        "201706": homedir
        + "/data_pool/Palm/MLY_data/DT_Res/post_mask_index_201706.tif",
        "201709": homedir
        + "/data_pool/Palm/MLY_data/DT_Res/post_mask_index_201709.tif",
    }

    valid_name = [
        "Johor",
        "Melaka",
        "Negeri",
        "Pahang",
        "Perak",
        "Selangor",
        "Trengganu",
    ]
    for index in palm_file_path.keys():
        print(palm_file_path[index])
        yearlabel = index[0:4]
        print(yearlabel)
        geo_dataset = gdal.Open(palm_file_path[index])
        geotransform = geo_dataset.GetGeoTransform()
        dst_proj = geo_dataset.GetProjection()
        cols = geo_dataset.RasterXSize
        rows = geo_dataset.RasterYSize
        Palm_mask = geo_dataset.GetRasterBand(1).ReadAsArray()

        # After post-process
        print("After post-process:")
        Palm_mask_ori = Palm_mask
        open_wid = 7
        close_wid = 5
        Palm_mask = Palm_mask_ori

        Palm_mask = Palm_mask.astype(float)
        key = "OC" + str(close_wid) + "_" + str(open_wid)
        # erode and morphology
        print("open", open_wid)
        print("close", close_wid)
        Palm_mask = cv2.morphologyEx(
            Palm_mask,
            cv2.MORPH_CLOSE,
            cv2.getStructuringElement(cv2.MORPH_RECT, (close_wid, close_wid)),
            iterations=1,
        )
        Palm_mask = cv2.morphologyEx(
            Palm_mask,
            cv2.MORPH_OPEN,
            cv2.getStructuringElement(cv2.MORPH_RECT, (open_wid, open_wid)),
            iterations=1,
        )

        palm_pix_num = Palm_mask[Palm_mask == 1].size
        palm_area = palm_pix_num * 400 / 10000.0
        MPOB_area = settings.MPOB_data[yearlabel][locateLabel]
        palm_overall_accracy = 100.0 * (palm_area - MPOB_area) / (MPOB_area)

        statearea = get_area_by_state(
            Palm_mask, geotransform, shapefile_path, yearlabel
        )
        print(Palm_mask.shape)

        print("Name\t\t\t\t" + "MPOB\t\t\t\t" + "Palm\t\t\t\t" + "Error")
        for stateRecord in statearea:
            stateName = stateRecord[0].split(" ")[0]
            if stateName in valid_name:
                print(
                    stateName
                    + "\t\t\t\t"
                    + str(round(stateRecord[1], 1))
                    + "\t\t\t\t"
                    + str(round(stateRecord[2], 1))
                    + "\t\t\t\t%"
                    + str(round(stateRecord[3], 1))
                )

        try:
            driver = gdal.GetDriverByName("GTiff")
        except Exception:
            print("Creat driver failed!")

        result_file = (
            "post_" + str(close_wid) + str(open_wid) + "_index_" + str(index) + ".tif"
        )
        print(result_file)

        try:
            palm_out = driver.Create(result_file, cols, rows, 1, gdal.GDT_Byte)
        except Exception as e:
            print("Creat output failed! %s", e)

        palm_out.SetGeoTransform(geotransform)
        palm_out.SetProjection(dst_proj)
        palm_out.GetRasterBand(1).WriteArray(Palm_mask)
        palm_out.FlushCache()
        palm_out = None
