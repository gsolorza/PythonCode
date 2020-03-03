#!/usr/bin/env python3

import json
from pprint import pprint
from tqdm import tqdm
import os
import sys
from netmiko import ConnectHandler
from device_list import unpack_device_list
from Connect import Connect_Manager

devices = unpack_device_list()

def write(filename, data, path):
    try:
        os.chdir(path)
        with open(filename, "w+") as output:
            output.write(data)
    except Exception as failure:
        print("THERE WAS AN ERROR TRYING TO WRITE THE FILE:\n--> {} <--".format(failure))

class Assessment():

    ios_commands = ["show version", "show clock"]

    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.project_folder = os.path.join(os.getcwd(), self.customer_name)

    def create_folder_structure(self):
        folders = ["CISCO_IOS"]
        print(self.project_folder)
        os.makedirs(self.project_folder, exist_ok=True)

        for folder in folders:
            device_type_folder = os.path.join(self.project_folder, folder)
            os.makedirs(device_type_folder, exist_ok=True)
            for command in Assessment.ios_commands:
                directory = command.replace(" ", "_")
                path = os.path.join(device_type_folder, directory)
                os.makedirs(path, exist_ok=True)

    def check_device_status(self, connection, commands):
        if "cisco_ios" in connection.device_type:
            device_type_folder = os.path.join(self.project_folder, connection.device_type.upper())
            for command in commands:
                json_output = connection.send_command(command, use_textfsm=True)
                json_string = json.dumps(json_output, indent=2)
                hostname = connection.base_prompt
                directory = command.replace(" ", "_")
                path = os.path.join(device_type_folder, directory)
                write(hostname, json_string, path)

customer = Assessment("Salcobrand")
customer.create_folder_structure()

for device in tqdm(devices, ascii=True):
    connection = Connect_Manager.connect(**device)
    customer.check_device_status(connection, customer.ios_commands)

