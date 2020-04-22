#!/usr/bin/env python3

import logging
from netmiko import ConnectHandler
from tqdm import tqdm
import json
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import AuthenticationException

logging.basicConfig(filename="Netmiko.log", level=logging.DEBUG)
logger = logging.getLogger("ConnectHandler")

class ConnectManager:

    @staticmethod
    def ssh(device_list, commands, textfsm=False):
        commands_output = []
        for device in tqdm(device_list, ascii=True):
            print(device["host"])
            try:
                device["global_delay_factor"] = 3
                connection = ConnectHandler(**device)

            except AuthenticationException:
                device["username"] = "ibustamante"
                device["password"] = "Salco.2020"
                connection = ConnectHandler(**device)

            except SSHException:
                try:
                    print("USING TELNET")
                    telnet_device = {}
                    telnet_device.update(device)
                    telnet_device["device_type"] = "cisco_ios_telnet"
                    connection = ConnectHandler(**telnet_device)

                except ConnectionResetError:
                    print("TELNET PASSWORD ERROR RESET")
                    telnet_device["username"] = "ibustamante"
                    telnet_device["password"] = "Salco.2020"
                    connection = ConnectHandler(**telnet_device)

                except NetMikoAuthenticationException:
                    print("TELNET PASSWORD ERROR")
                    telnet_device["username"] = "ibustamante"
                    telnet_device["password"] = "Salco.2020"
                    connection = ConnectHandler(**telnet_device)

                except Exception as failure:
                    print("THERE IS AN ERROR WITH THE DEVICE:\n--> {} <-- and the error was {}".format(device["host"], failure))
                    continue

                finally:
                    try:
                        connection.write_channel("enable\n")
                        connection.write_channel("Red3s#63_1")
                        hostname = connection.base_prompt
                        print(hostname)
                        dcom = {hostname: []}
                        for command in commands:
                            print("Collecting Information: "+command)
                            output_list = connection.send_command(command, use_textfsm=textfsm)
                            cm = command.replace(" ", "_")
                            dcom[hostname].append({cm: output_list})
                        commands_output.append(dcom)
                        connection.disconnect()
                    except Exception as failure:
                        print("THERE IS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <-- and the error was {}".format(device["host"], failure))
                        continue


            except Exception as failure:
                print("THERE IS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <-- and the error was {}".format(device["host"], failure))
                continue
            
            finally:
                try:
                    connection.write_channel("enable\n")
                    connection.write_channel("Red3s#63_1")
                    hostname = connection.base_prompt
                    print(hostname)
                    dcom = {hostname: []}
                    for command in commands:
                        print("Collecting Information: "+command)
                        output_list = connection.send_command(command, use_textfsm=textfsm)
                        cm = command.replace(" ", "_")
                        dcom[hostname].append({cm: output_list})
                    commands_output.append(dcom)
                    connection.disconnect()
                except Exception as failure:
                    print("THERE IS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <-- and the error was {}".format(device["host"], failure))
                    continue
                    

        return commands_output






