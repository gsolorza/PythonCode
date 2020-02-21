#!/usr/bin/env python3

from netmiko import ConnectHandler
from Assessment.device_list import unpack_device_list
import Assessment.get_config
import Assessment.get_interface_rates
from tqdm import tqdm

device_list = unpack_device_list()

def connect(device_list, task):
    for device in tqdm(device_list, ascii=True):
        try:
            connection = ConnectHandler(**device)
            task(connection)
        except:
            print("SOMETHING WENT WRONG CONNECTING TO HOST "+device["host"]+" VIA SSH")


if __name__ == "__main__":
    connect(device_list, get_config)