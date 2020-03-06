#!/usr/bin/env python3

from netmiko import ConnectHandler
from tqdm import tqdm
import json

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
                output_list = connection.send_command(command, use_textfsm=True)
                cm = command.replace(" ", "_")
                if isinstance(output_list, list):
                    dcom[hostname].append({cm: json.dumps(output_list[0])})
                elif isinstance(output_list, str):
                    dcom[hostname].append({cm: output_list})
            commands_output.append(dcom)
                
        return commands_output






