#!/usr/bin/env python3

def get_hostname(connection):
    if connection.device_type == "cisco_ios":
        output = connection.send_command("show run | sec hostname")
        hostname = output.strip("hostname ")
        return hostname
    elif connection.device_type == "cisco_xr":
        output = connection.send_command("show run hostname")
        hostname = output.split("\n")[1].strip("hostname ")
        return hostname