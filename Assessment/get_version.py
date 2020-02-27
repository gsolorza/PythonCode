#!usr/bin/env python3

import json

def get_version(connection):
    output = connection.send_command("show version", use_textfsm=True)
    print(json.dumps(output, indent=2))