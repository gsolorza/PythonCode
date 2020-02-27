#!/usr/bin/env python3

from netmiko import ConnectHandler
from device_list import unpack_device_list
from get_config import get_config
from get_interface_rates import get_interface_usage
from get_hostname import get_hostname
from tqdm import tqdm
from pprint import pprint

device_list = unpack_device_list()

def connect(device_list):
    for device in tqdm(device_list, ascii=True):
        try:
            connection = ConnectHandler(**device)
            hostname = get_hostname(connection)
            # get_config(connection, hostname)
            pprint(get_interface_usage(connection))
            
        except:
            print("SOMETHING WENT WRONG CONNECTING TO HOST "+device["host"]+" VIA SSH")


if __name__ == "__main__":
    connect(device_list)