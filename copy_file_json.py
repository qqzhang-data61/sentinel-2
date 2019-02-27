#!/usr/bin/env python3
import subprocess
import json
from pathlib import Path

file_name = "/home/tq/data_pool/Palm/data_json/palm_201709_water.json"

date_str = Path(file_name).stem.split("_")[1]

with open(file_name, "r") as fp:
    process_list = json.load(fp)

tmp_dir = "/tmp/water"

count = 1
for tmp in process_list:
    print("\nprocess->", count, tmp)
    count += 1
    tq_server = tmp.split("/")[0]
    if tq_server == "tq-data04" and date_str in ["201703", "201706"]:
        tq_server = "tq-data05"
    elif tq_server == "tq-data04" and date_str in ["201709", "201712"]:
        tq_server = "tq-data04"
    else:
        pass
    orbit_number = tmp.split("/")[2]
    data_id = tmp.split("/")[-1].split("_")[-1][0:4]
    run_flag = subprocess.run(
        [
            "sh",
            "/home/tq/workspace/sentinel-1/copy_img.sh",
            tq_server,
            orbit_number,
            data_id,
            tmp_dir,
        ]
    )
    if run_flag.returncode == 0:
        print("copy data sucess.")
    else:
        print("copy data failed!")
