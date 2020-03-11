#!/usr/bin/env python3

from netmiko import ConnectHandler
from tqdm import tqdm
import json
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import AuthenticationException

def send_all_commands(hostname, commands, connection):
    dcom = {hostname: []}
    for command in commands:
        output_list = connection.send_command(command, use_textfsm=textfsm)
        cm = command.replace(" ", "_")
        dcom[hostname].append({cm: output_list})
    return dcom

class ConnectManager:

    @staticmethod
    def ssh(device_list, commands, textfsm=False):
        commands_output = []
        for device in tqdm(device_list, ascii=True):
            try:
                connection = ConnectHandler(**device)

            except AuthenticationException:
                device["username"] = "cisco"
                device["password"] = "cisco"
                connection = ConnectHandler(**device)

            except SSHException:
                try:
                    telnet_device = {}
                    telnet_device.update(device)
                    telnet_device["device_type"] = "cisco_ios_telnet"
                    connection = ConnectHandler(**telnet_device)

                except ConnectionResetError:
                    telnet_device["username"] = "cisco"
                    telnet_device["password"] = "cisco"
                    connection = ConnectHandler(**telnet_device)    
                    
                finally:
                    hostname = connection.base_prompt
                    dcom = {hostname: []}
                    for command in commands:
                        output_list = connection.send_command(command, use_textfsm=textfsm)
                        cm = command.replace(" ", "_")
                        dcom[hostname].append({cm: output_list})
                    commands_output.append(dcom)

            except Exception as failure:
                print("THERE WAS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <--".format(failure))
            
            finally:
                try:
                    hostname = connection.base_prompt
                    dcom = {hostname: []}
                    for command in commands:
                        output_list = connection.send_command(command, use_textfsm=textfsm)
                        cm = command.replace(" ", "_")
                        dcom[hostname].append({cm: output_list})
                    commands_output.append(dcom)
                except Exception as failure:
                    print("THERE WAS AN ERROR TRYING TO CREATE DEVICE DATA:\n--> {} <--".format(failure))
                    
        return commands_output






