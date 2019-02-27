#!/usr/bin/#!/usr/bin/env python3
import os
import time
import glob
import json

home_dir = os.path.expanduser("~")


def find_orbit_data(year: str, orbit: int) -> list:
    """
    Function:
        give the orbit, get all data
    Input:
        orbit int = [1 175]
    """
    # find all data
    file_path = os.path.join(
        home_dir, "*/sentinel1_GRDH/", str(orbit), "*_GRDH_1SDV_" + year + "*"
    )
    tmp_list = glob.glob(file_path)
    if tmp_list:
        return tmp_list
    else:
        return None


def save_result(result_file: str, data_list: list) -> str:
    """
        save every data in json and return the path
    """
    with open(result_file, "w") as fp:
        json.dump(data_list, fp, ensure_ascii=False, indent=2)
    print("result_file total data", len(data_list))


if __name__ == "__main__":

    base_name = "/home/tq/data2/citrus/sichuan_S1/orbit_list_2018.json"
    orbit = [55, 157, 128]
    for tmp in orbit:
        tmp_list = find_orbit_data("2018", tmp)
        result_file = base_name.replace("orbit", "orbit_" + str(tmp) + "_")
        save_result(result_file, tmp_list)
