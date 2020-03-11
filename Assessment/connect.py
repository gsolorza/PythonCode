#!/usr/bin/env python3

from netmiko import ConnectHandler
from tqdm import tqdm
import json
from paramiko.ssh_exception import SSHException

class ConnectManager:

    @staticmethod
    def ssh(device_list, commands, textfsm=False):
        commands_output = []
        for device in tqdm(device_list, ascii=True):
            try:
                connection = ConnectHandler(**device)
                hostname = connection.base_prompt
                dcom = {hostname: []}
                for command in commands:
                    output_list = connection.send_command(command, use_textfsm=textfsm)
                    cm = command.replace(" ", "_")
                    dcom[hostname].append({cm: output_list})
                commands_output.append(dcom)
                
            except SSHException:
                telnet_device = {}
                telnet_device.update(device)
                telnet_device["device_type"] = "cisco_ios_telnet"
                connection = ConnectHandler(**telnet_device)
                hostname = connection.base_prompt
                dcom = {hostname: []}
                for command in commands:
                    output_list = connection.send_command(command, use_textfsm=textfsm)
                    cm = command.replace(" ", "_")
                    dcom[hostname].append({cm: output_list})
                commands_output.append(dcom)

            except Exception as failure:
                print("THERE WAS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <--".format(failure))
     
                
        return commands_output






