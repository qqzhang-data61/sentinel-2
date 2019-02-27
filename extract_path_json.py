#!/usr/bin/env python3
import sys
import os
import pprint
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
printer = pprint.PrettyPrinter(indent=3)

file_name = "/home/tq/data_pool/china_crop/tianchang/sentinel1_process.json"

with open(file_name, "r") as fp:
    process_all_dict = json.load(fp)
process_dict = process_all_dict["scenes"]

process_list = {"scenes": [f for f in process_dict if "_GRDH_" in f["relative_path"]]}
printer.pprint(process_list)

result_name = "/home/tq/data_pool/china_crop/tianchang/sentinel1.json"
with open(result_name, "w") as fp1:
    json.dump(process_list, fp1, ensure_ascii=False, indent=2)
