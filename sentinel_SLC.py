#!/usr/bin/env python3
import os
import time
import shutil
import subprocess
import xml.etree.ElementTree as ET


class SentinelSLC:
    def __init__(self, process_path, result_root):
        self.result_root = result_root
        self.home_dir = os.path.expanduser("~")  # docker must be processed by user tq

        self.process_file = os.path.join(
            os.path.expanduser("~"), process_path
        )  # /home/tq/tq-data0*/sentinel1/*/*.zip

        self.local_path = os.path.join(
            self.home_dir, "tq-tmp", process_path.split("/S1")[0]
        )  # /home/tq/tq-tmp/tq-data0*/sentinel1/*

        self.reult_file_suffix = os.path.join(
            "sentinel1_GRD",
            process_path.split("/sentinel1/")[-1]
            .replace("SLC", "GRDH")
            .replace(".zip", "_Orb_Deb_ML_SRGR_Cal_Spk_TF_TC.tif"),
        )  # sentinel1_GRD/*/*.tif

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
            tmp_path = os.path.join(self.home_dir, tmp_server, self.reult_file_suffix)
            if os.path.exists(tmp_path):
                return os.path.split(tmp_path), True
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
        peocess_xml = self.local_path + "/process.xml"  # set xml path

        process_result_path = os.path.join(
            self.local_path, os.path.split(self.reult_file_suffix)[-1]
        )  # set result path

        base_xml = os.path.join(self.SLC_aux_dir, "graph-test-min.xml")  # get base xml
        tree = ET.ElementTree(file=base_xml)
        root = tree.getroot()
        for child in root.iter(tag="file"):  # set new xml for process
            if child.text == "process_file":
                child.text = self.process_file
            elif child.text == "result_file":
                child.text = process_result_path
            else:
                print("please check the process xml!")
                return None, False
        try:
            tree.write(peocess_xml)
            return peocess_xml, True
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
        process_flag = subprocess.run(["gpt", process_xml])
        if process_flag.returncode == 0:
            print("Raw data process sucess.", self.process_file)
            result_path = os.path.join(
                self.home_dir, self.result_root, self.reult_file_suffix
            )
            try:
                shutil.move(self.local_path, result_path)
                shutil.rmtree(self.local_path)
                return result_path, True
            except Exception as e:
                print(e)
                return None, False
        else:
            print("Raw data process failed!", self.process_file)
            return None, False

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
