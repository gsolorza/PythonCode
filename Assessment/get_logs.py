#!/usr/bin/env python3

import json

def get_clock(connection):
    output = connection.send_command("show clock", use_textfsm=True)
    print(json.dumps(output, indent=2))

def get_logs(connection):
    output = connection.send_command("show logging", use_textfsm=True)
    print(json.dumps(output, indent=2))