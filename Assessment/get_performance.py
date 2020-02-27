#!/usr/bin/env python3

import json

def get_cpu(connection):
    output = connection.send_command("show processes cpu", use_textfsm=True)
    print(json.dumps(output, indent=2))

def get_memory(connection):
    output = connection.send_command("show processes memory sorted", use_textfsm=True)
    print(json.dumps(output, indent=2))

def get_storage(connection):
    output = connection.send_command("dir", use_textfsm=True)
    print(json.dumps(output, indent=2))

def get_environment(connection):
    output = connection.send_command("show env", use_textfsm=True)
    print(json.dumps(output, indent=2))