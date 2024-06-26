#!/usr/bin/env python3

import json
from pprint import pprint
import os
import sys
from device_list import unpack_device_list
from connect import ConnectManager as connect
from dataframestest import create_dataframes
import inventory
import pandas as pd

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

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.project_folder = os.path.join(os.getcwd(), self.customer_name)
        os.makedirs(self.project_folder, exist_ok=True)

    def find_correct_folder(self, folder_name):
        for subdir, dirs, files in os.walk(self.project_folder):
            for direct in dirs:
                if direct == folder_name:
                    return os.path.join(subdir, direct)
    
    def update_data_file(self, new_data, devices_data_file):

        if devices_data_file:
            device_command_list = {}
            for device_dict in devices_data_file:
                for device, device_data in device_dict.items():
                    device_command_list[device] = []
                    for data in device_data:
                        for command in data.keys():
                            device_command_list[device].append(command)
            
            for dict1 in new_data:
                for host1, data_list1 in dict1.items():
                    if host1 not in device_command_list.keys():
                        devices_data_file.append(dict1)
                        continue
                    for dict2 in devices_data_file:
                        for host2 in dict2.keys():
                            if host1 == host2:
                                for data in data_list1:
                                    for command in data.keys():
                                        if command not in device_command_list[host2]:
                                            device_command_list[host2].append(command)
                                            dict2[host2].append(data)
                            else:
                                pass

            return devices_data_file

        else:
            return new_data

    def write_to_excel(self, folder_name, dataframes):
        for df_type in dataframes.keys():
            if "device_dataframe" == df_type:
                for hostname in dataframes[df_type].keys():
                    os.chdir(self.find_correct_folder(hostname))
                    writer = pd.ExcelWriter(hostname+".xlsx", engine="xlsxwriter")
                    for data in dataframes[df_type][hostname]:
                        for command, df_dev in data.items():
                            df = pd.DataFrame(df_dev)
                            df.to_excel(writer, command)
                    writer.save()
            elif "command_dataframe" == df_type:
                writer = pd.ExcelWriter("global_config.xlsx", engine="xlsxwriter")
                for command, df_cmd in dataframes[df_type].items():
                    os.chdir(self.find_correct_folder(folder_name))
                    df = pd.DataFrame(df_cmd)
                    df.to_excel(writer, command)
                writer.save()
    
    def create_folder_structure(self, folder_name, data):

        device_type_folder = os.path.join(self.project_folder, folder_name)
        os.makedirs(device_type_folder, exist_ok=True)
        if "devices_data.json" in os.listdir(device_type_folder):
            with open(device_type_folder+"/devices_data.json") as prev_data:
                previous_data = json.load(prev_data)
                dev_data = self.update_data_file(data, previous_data)

        else:
            dev_data = data

        write("devices_data", device_type_folder, dev_data)
        for device in dev_data:
            for hostname, device_data in device.items():
                path = os.path.join(device_type_folder, hostname)
                os.makedirs(path, exist_ok=True)
                for data in device_data:
                    for command, output in data.items():
                            write(command, path, output)

        return dev_data

customer = Assessment("netvoix")
device_list = inventory.Devices("device_list.csv")
device_list.unpack_device_list()

for device_type, data in device_list.global_devices.items():
    devices_data = connect.ssh(data["device_list"], data["commands"], textfsm=True)
    devices_data = customer.create_folder_structure(device_type, devices_data)
    dataframes = create_dataframes(devices_data)
    customer.write_to_excel(device_type, dataframes)



