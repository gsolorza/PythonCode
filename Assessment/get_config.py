#!/usr/bin/env python3

from device_list import unpack_device_list, connect
from tqdm import tqdm

device_list = unpack_device_list()

for device in tqdm(device_list, ascii=True):
    connection = connect(**device)
    try:
        output = connection.send_command("show running-config")
    except:
        continue
    hostname = connection.find_prompt().strip("#")
    try:
        with open(hostname+".log", "w") as config_file:
            config_file.write(output)
    except:
        print("SOMETHING WENT WRONG CREATING THE FILE")