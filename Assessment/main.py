#!/usr/bin/env python3

from netmiko import ConnectHandler
from device_list import unpack_device_list
from get_config import get_config
from get_interface_rates import get_interface_status, get_interfaces
from get_hostname import get_hostname
from get_inventory import get_inventory
from get_performance import get_cpu, get_memory, get_storage, get_environment
from get_logs import get_logs, get_clock
from get_version import get_version
from tqdm import tqdm
from pprint import pprint

device_list = unpack_device_list()

def connect(device_list):
    for device in tqdm(device_list, ascii=True):
        try:
            connection = ConnectHandler(**device)       
        except:
            print("SOMETHING WENT WRONG CONNECTING TO HOST "+device["host"]+" VIA SSH")
        print(connection.host)
        get_interface_status(connection)

if __name__ == "__main__":
    connect(device_list)

