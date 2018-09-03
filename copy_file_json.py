#!/usr/bin/env python3
import subprocess
import json


file_name = "/home/tq/data_pool/Palm/data_json/palm_201712_final.json"

with open(file_name, "r") as fp:
    process_list = json.load(fp)

tmp_dir = "/tmp/palm_201712"

for tmp in process_list:
    print(tmp)
    tq_server = tmp.split("/")[0]
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
        print("clip data sucess.")
    else:
        print("clip data failed!")
