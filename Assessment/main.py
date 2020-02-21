#!/usr/bin/env python3

from netmiko import ConnectHandler
from device_list import unpack_device_list
from get_interface_rates import get_interface_rates
from get_config import get_config
from tqdm import tqdm

device_list = unpack_device_list()

def connect(device_list, task):
    for device in tqdm(device_list, ascii=True):
        try:
            connection = ConnectHandler(**device)
            task(connection)
        except:
            print("SOMETHING WENT WRONG CONNECTING TO HOST "+device["host"]+" VIA SSH")


connect(device_list, get_config)