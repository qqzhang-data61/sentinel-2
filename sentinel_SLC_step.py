#!/usr/bin/env python3
import os
import time

# import shutil
import subprocess
import xml.etree.ElementTree as ET


class SentinelSLC:
    def __init__(self, process_path, result_root):
        self.result_root = result_root
        self.home_dir = "/home/tq"  # docker must be processed by user tq

        self.process_file = os.path.join(
            self.home_dir, process_path
        )  # /home/tq/tq-data0*/sentinel1/*/*.zip

        self.local_path = os.path.join(
            self.home_dir, "tq-tmp", process_path.split("/S1")[0]
        )  # /home/tq/tq-tmp/tq-data0*/sentinel1/*

        self.result_file_part1 = os.path.join(
            "sentinel1_GRD",
            process_path.split("/sentinel1/")[-1]
            .replace("SLC", "GRDH")
            .replace(".zip", "_part1.dim"),
        )  # sentinel1_GRD/*/*._part1.dim

        self.result_file_part2 = os.path.join(
            "sentinel1_GRD",
            process_path.split("/sentinel1/")[-1]
            .replace("SLC", "GRDH")
            .replace(".zip", "_part2.dim"),
        )  # sentinel1_GRD/*/*._part2.dim

        self.result_file_part3 = os.path.join(
            "sentinel1_GRD",
            process_path.split("/sentinel1/")[-1]
            .replace("SLC", "GRDH")
            .replace(".zip", "_part3.tif"),
        )  # sentinel1_GRD/*/*._part3.tif

        self.server_list = ["tq-data03", "tq-data04", "tq-data02", "tq-data01"]
        self.SLC_aux_dir = os.path.join(self.home_dir, "data_pool/SLC_Preprocess_aux")

    def check_process_status(self) -> (str, bool):
        """
        Function:
            Check whether the data has been processed
        output:
            str, True: return result path
            None, False: return None and false
        """
        # check the result
        for tmp_server in self.server_list:
            tmp_path = os.path.join(self.home_dir, tmp_server, self.result_file_part3)
            if os.path.exists(tmp_path):
                return os.path.split(tmp_path)[0], True
            else:
                continue
        return None, False

    def unzip_data_local(self) -> (str, bool):
        """
        Function:
            unzip the data to local path
        input:
            process data path
            tq-data04/sentinel1/3/S1A_IW_SLC__1SDV_20180517T220619_20180517T220646_021950_025ECB_DA3B.zip
        output:
            (False): unzip failue
            (Ture): return local path:/home/tq/tq-tmp/tq-data*/sentinel1/3
        """

        #  check the raw data
        if not os.path.exists(self.process_file):
            print("%s process file does not exist!" % self.process_file)
            return False
        else:
            if not os.path.exists(self.local_path):
                os.makedirs(self.local_path)

            # creat local path to process the data
            process_flag = subprocess.run(
                ["unzip", self.process_file, "-d", self.local_path]
            )
            if process_flag.returncode == 0:
                print("Raw data unzip sucess.", self.process_file)
                return True
            else:
                print("Raw data unzip!", self.process_file)
                return False

    def creat_process_xml(self) -> (str, bool):
        """
        Function:
            unzip the data to local path
        input:
            local_path /home/tq/tq-tmp/sentinel1/2
        output:
            False: creat xml failue
            True: creat xml sucess
        """
        os.chdir(self.local_path)
        part1_xml = self.local_path + "/part1.xml"
        part2_xml = self.local_path + "/part2.xml"
        part3_xml = self.local_path + "/part3.xml"

        part1_result_path = os.path.join(
            self.local_path, os.path.split(self.result_file_part1)[-1]
        )  # set result path

        base_part1_xml = os.path.join(
            self.SLC_aux_dir, "SLC_to_GRD_part1.xml"
        )  # get base xml

        tree = ET.ElementTree(file=base_part1_xml)
        root = tree.getroot()
        for child in root.iter(tag="file"):  # set new xml for process
            if child.text == "process_file":
                child.text = self.process_file
                continue
            elif child.text == "result_file":
                child.text = part1_result_path
                continue
            else:
                print("please check the process part1 xml!")
                return None, False
        try:
            tree.write(part1_xml)
        except Exception as e:
            print(e)
            return None, False

        part2_result_path = os.path.join(
            self.local_path, os.path.split(self.result_file_part2)[-1]
        )  # set result path

        base_part2_xml = os.path.join(
            self.SLC_aux_dir, "SLC_to_GRD_part2.xml"
        )  # get base xml

        tree = ET.ElementTree(file=base_part2_xml)
        root = tree.getroot()
        for child in root.iter(tag="file"):  # set new xml for process
            if child.text == "process_file":
                child.text = part1_result_path
                continue
            elif child.text == "result_file":
                child.text = part2_result_path
                continue
            else:
                print("please check the process part2 xml!")
                return None, False
        try:
            tree.write(part2_xml)
        except Exception as e:
            print(e)
            return None, False

        part3_result_path = os.path.join(
            self.local_path, os.path.split(self.result_file_part3)[-1]
        )  # set result path

        base_part3_xml = os.path.join(
            self.SLC_aux_dir, "GRD_Terrain.xml"
        )  # get base xml

        tree = ET.ElementTree(file=base_part3_xml)
        root = tree.getroot()
        for child in root.iter(tag="file"):  # set new xml for process
            if child.text == "process_file":
                child.text = part2_result_path
                continue
            elif child.text == "result_file":
                child.text = part3_result_path
                continue
            else:
                print("please check the process part3 xml!")
                return None, False
        try:
            tree.write(part3_xml)
            process_xml = [part1_xml, part2_xml, part3_xml]
            return process_xml, True
        except Exception as e:
            print(e)
            return None, False

    def gpt_process(self, process_xml) -> (str, bool):
        """
        Function:
            use gpt to process sentinel 1
        input:
            process-xml is based on config_xml /data_pool/SLC_preprocess_aux/*.xml
        output:
            None, False: process failue
            str, True: return the path
        """

        for xml in process_xml:
            if "part1.xml" in xml:
                process_flag = subprocess.run(["gpt", xml])
                if process_flag.returncode == 0:
                    print("part1 process sucess.", self.process_file)
                    continue
                else:
                    print("part1 process failed!", self.process_file)
                    return None, False
            else:
                continue

            if "part2.xml" in xml:
                process_flag = subprocess.run(["gpt", xml])
                if process_flag.returncode == 0:
                    print("part2 process sucess.", self.process_file)
                    continue
                else:
                    print("part2 process failed!", self.process_file)
                    return None, False
            else:
                continue

            if "part3.xml" in xml:
                process_flag = subprocess.run(["gpt", xml])
                if process_flag.returncode == 0:
                    print("part3 process sucess.", self.process_file)
                    return "haha", True
                else:
                    print("part3 process failed!", self.process_file)
                    return None, False
            else:
                continue

    def go_process(self) -> int:
        """
        Function:
            ****************sentinel1 SLC preprocess****************
            Step 1: check process data status
            Step 2: unzip raw  data
            Step 3: creat process xml
            Step 4: gpt process
        ouput:
            process_status
            0: sucess
            1: data has been processed
            2: unzip data has problem
            3: creat xml failed
            4: gpt falied
        """

        # Step 1
        print(self.process_file)
        print("Step 1: will be check process data status!")
        result_path, flag = self.check_process_status()
        if flag:
            process_status = 1
            return result_path, process_status
        else:
            print("Step 2: will be unzip raw data")

        # Step 2
        flag = self.unzip_data_local()
        if not flag:
            process_status = 2
            return None, process_status
        else:
            print("Step 3: will be creat process xml!")

        # Step 3
        process_xml, flag = self.creat_process_xml()
        if not flag:
            process_status = 3
            return None, process_status
        else:
            print("Step 4: gpt process.")

        # Step 4
        result_path, flag = self.gpt_process(process_xml)
        if not flag:
            process_status = 4
            return None, process_status
        else:
            process_status = 0
            print(self.process_file, "finished.")
            return result_path, process_status


if __name__ == "__main__":

    start = time.time()

    result_root = "tq-data04"
    process_file = "tq-data04/sentinel1/3/S1A_IW_SLC__1SDV_20180517T220619_20180517T220646_021950_025ECB_DA3B.zip"

    SLC = SentinelSLC(process_file, result_root)
    # flag = SLC.creat_process_xml("/home/tq/tq-tmp/tq-data04/sentinel1/3")
    flag = SLC.go_process()
    print("process_status:", flag)
    end = time.time()
    print("Task runs %0.2f seconds" % (end - start))
