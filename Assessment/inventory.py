#!/usr/bin/env python3

import csv

class Devices:

    global_devices = {}
    commands = {
        "cisco_ios": 
        [
            "show version"
        ],
        "cisco_nxos": 
        [
            "show version"
        ],
        "cisco_xr": 
        [
            "show version"
        ]
    }

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def unpack_device_list(self):
        with open(self.csv_file) as file:
            devices = csv.DictReader(file)
            for dev in devices:
                device_type = dev["device_type"]
                try:
                    self.global_devices[device_type]["device_list"].append(dev)
                except KeyError:
                    self.global_devices[device_type] = {"device_list": [], "commands": []}
                    self.global_devices[device_type]["device_list"].append(dev)
                    self.global_devices[device_type]["commands"].extend(self.commands[device_type])

            




