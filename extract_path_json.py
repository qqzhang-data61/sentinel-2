#!/usr/bin/env python3
import sys
import os
import pprint
import json

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
printer = pprint.PrettyPrinter(indent=3)

file_name = "/home/tq/data_pool/Palm/data_json/palm_201706_tq_20180831.json"

with open(file_name, "r") as fp:
    process_all_dict = json.load(fp)
process_dict = process_all_dict["scenes"]

process_list = [f["relative_path"] for f in process_dict]
print(len(process_list))

process_set = set(process_list)
process_list = list(process_set)
process_list.sort()

print(len(process_list))
printer.pprint(process_list)

result_name = "/home/tq/data_pool/Palm/data_json/palm_201706_20180831.json"
with open(result_name, "w") as fp1:
    json.dump(process_list, fp1, ensure_ascii=False, indent=2)
