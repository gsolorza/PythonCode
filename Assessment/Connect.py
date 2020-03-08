#!/usr/bin/env python3

from netmiko import ConnectHandler
from tqdm import tqdm

class ConnectManager:

    @staticmethod
    def ssh(device_list, commands):
        commands_output = []
        for device in tqdm(device_list, ascii=True):
            try:
                connection = ConnectHandler(**device)
            except Exception as failure:
                print("THERE WAS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <--".format(failure))
            hostname = connection.base_prompt
            dcom = {hostname: []}
            for command in commands:
                list_output = connection.send_command(command, use_textfsm=True)
                cm = command.replace(" ", "_")
                dcom[hostname].append({cm: list_output[0]})
            commands_output.append(dcom)
                
        return commands_output


