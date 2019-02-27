#!/usr/bin/env python3
import sys
import os
import pprint
import json
import xlsxwriter

from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))
printer = pprint.PrettyPrinter(indent=3)

file_name = "/home/tq/data_pool/TF_DATA/palm/20171226/palm_20171226.json"

with open(file_name, "r") as fp:
    process_dict = json.load(fp)
out_result = sorted(process_dict["palm"])
printer.pprint(out_result)

out_result = [(f[0], f[1]["1"]) for f in out_result if "136" in f[0]]

# out xlsx
out_xlsx = Path(file_name).with_name(Path(file_name).stem + ".xlsx")
workbook = xlsxwriter.Workbook(out_xlsx)
worksheet = workbook.add_worksheet()
row = 0
col = 0
for item, cost in out_result:
    worksheet.write(row, col, item)
    worksheet.write(row, col + 1, cost)
    row += 1
workbook.close()
