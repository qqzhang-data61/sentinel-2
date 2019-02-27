import gdal
import cv2
import numpy as np

before_tif_name = "/home/tq/data_pool/Flood/water_test/dem/water_201709_Clip.tif"
after_tif_name = "/home/tq/data_pool/Flood/water_test/dem/water_201712_Clip.tif"
try:
    before_set = gdal.Open(before_tif_name)
    before_tif = before_set.GetRasterBand(1).ReadAsArray()
except Exception as e:
    print(e)
try:
    after_set = gdal.Open(after_tif_name)
    after_tif = after_set.GetRasterBand(1).ReadAsArray()

except Exception as e:
    print(e)
# erode and morphology
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
tif_erosion = cv2.erode(after_tif, kernel)
tif_dilation = cv2.dilate(before_tif, kernel)
mask_subtract = np.subtract(tif_erosion, tif_dilation)
mask = np.equal(mask_subtract, 1)

# get information for geo
geotransform = before_set.GetGeoTransform()
dst_proj = before_set.GetProjection()
[cols, rows] = before_tif.shape

# creat output
print("output result data!")
try:
    driver = gdal.GetDriverByName("GTiff")
except Exception as e:
    print(e)

file_name = "/home/tq/data_pool/Flood/water_test/dem/water_mask.tif"
try:
    output = driver.Create(file_name, rows, cols, 1, gdal.GDT_Byte)
except Exception as e:
    print(e)

output.SetGeoTransform(geotransform)
output.SetProjection(dst_proj)
output.GetRasterBand(1).WriteArray(mask)
output.GetRasterBand(1).SetNoDataValue(0)
output.FlushCache()
output = None

file_name = "/home/tq/data_pool/Flood/water_test/dem/water_201709P.tif"
try:
    output = driver.Create(file_name, rows, cols, 1, gdal.GDT_Byte)
except Exception as e:
    print(e)

output.SetGeoTransform(geotransform)
output.SetProjection(dst_proj)
output.GetRasterBand(1).WriteArray(tif_dilation)
output.GetRasterBand(1).SetNoDataValue(0)
output.FlushCache()
output = None


file_name = "/home/tq/data_pool/Flood/water_test/dem/water_201712P.tif"
try:
    output = driver.Create(file_name, rows, cols, 1, gdal.GDT_Byte)
except Exception as e:
    print(e)

output.SetGeoTransform(geotransform)
output.SetProjection(dst_proj)
output.GetRasterBand(1).WriteArray(tif_erosion)
output.GetRasterBand(1).SetNoDataValue(0)
output.FlushCache()
output = None
