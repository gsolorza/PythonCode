#!/usr/bin/env python3

import json
from pprint import pprint
import os
import sys
from device_list import unpack_device_list
from connect import ConnectManager as connect
from dataframestest import create_dataframes
import pandas as pd

devices = unpack_device_list()

def write(filename, path, data):
    if isinstance(data, list):
        try:
            os.chdir(path)
            with open(filename+".json", "w+") as output:
                json.dump(data, output)
        except Exception as failure:
            print("THERE WAS AN ERROR TRYING TO WRITE THE FILE:\n--> {} <--".format(failure))
    elif isinstance(data, str):
        try:
            os.chdir(path)
            with open(filename+".log", "w+") as output:
                output.write(data)
        except Exception as failure:
            print("THERE WAS AN ERROR TRYING TO WRITE THE FILE:\n--> {} <--".format(failure))

class Assessment:

    ios_commands = ["show interfaces", "show interface status", "show version", "show running-config", "show logging", "show process cpu", "show process memory sorted"]

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.project_folder = os.path.join(os.getcwd(), self.customer_name)
        os.makedirs(self.project_folder, exist_ok=True)

    def find_correct_folder(self, folder_name):
        for subdir, dirs, files in os.walk(self.project_folder):
            for direct in dirs:
                if direct == folder_name:
                    return os.path.join(subdir, direct)

    def write_to_excel(self, dataframes):
        for df_type in dataframes.keys():
            if "device_dataframe" == df_type:
                for hostname in dataframes[df_type].keys():
                    os.chdir(self.find_correct_folder(hostname))
                    writer = pd.ExcelWriter(hostname+".xlsx", engine="xlsxwriter")
                    for data in dataframes[df_type][hostname]:
                        for command, df_dev in data.items():
                            df = pd.DataFrame(df_dev)
                            print(df)
                            df.to_excel(writer, command)
                    writer.save()
            elif "command_dataframe" == df_type:
                writer = pd.ExcelWriter("global_config.xlsx", engine="xlsxwriter")
                for command, df_cmd in dataframes[df_type].items():
                    os.chdir(self.find_correct_folder("cisco_ios"))
                    df = pd.DataFrame(df_cmd)
                    print(df)
                    df.to_excel(writer, command)
                writer.save()
    
    def create_folder_structure(self, devices_data):
        folders = set([dev["device_type"] for dev in devices])

        for folder in folders:
            device_type_folder = os.path.join(self.project_folder, folder)
            os.makedirs(device_type_folder, exist_ok=True)
            write("devices_data", device_type_folder, devices_data)
        for device in devices_data:
            for hostname, device_data in device.items():
                path = os.path.join(device_type_folder, hostname)
                os.makedirs(path, exist_ok=True)
                for data in device_data:
                    for command, output in data.items():
                            write(command, path, output)



customer = Assessment("Salcobrand")
devices_data = connect.ssh(devices, customer.ios_commands, textfsm=True)
customer.create_folder_structure(devices_data)
dataframes = create_dataframes(devices_data)
customer.write_to_excel(dataframes)



