#!/usr/bin/env python3
# import ogr
import subprocess

inraster = "/home/tq/tq-data01/sentinel_GRD/256/S1A_IW_SLC__1SDV_20151031T215929_20151031T215956_008402_00BDE6_D2A9_20180810T151724/palm_test/S1A_IW_GRDH__1SDV_20151031T215929_20151031T215956_008402_00BDE6_D2A9_GRD_TC_DB_palm_20180810T153015.tif"
outraster = "/home/tq/tq-data01/sentinel_GRD/256/S1A_IW_SLC__1SDV_20151031T215929_20151031T215956_008402_00BDE6_D2A9_20180810T151724/palm_test/gdal_test_8_"

for i in range(99, 1000, 100):
    tmp_file = outraster + str(i) + ".tif"
    IDN_flag = subprocess.run(
        ["gdal_sieve.py", "-st", str(i), "-8", inraster, tmp_file]
    )
    if IDN_flag.returncode == 0:
        print(f"{i} data sucess.")
    else:
        print(f"{i} data failed!")
