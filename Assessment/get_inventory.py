#!/usr/bin/env python3

from pprint import pprint
import json

def get_inventory(connection):
    if "cisco_ios" in connection.device_type:
        print(connection.device_type)
        output = connection.send_command("show inventory", use_textfsm=True)
        print(json.dumps(output, indent=2))
    elif "cisco_xr" in connection.device_type:
        output = connection.send_command("admin show inventory", use_textfsm=True)
        print(json.dumps(output, indent=2))
    else:
        pass