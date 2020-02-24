#!/usr/bin/env python3

def get_config(connection, hostname):
    output = connection.send_command("show running-config")
    try:
        with open(hostname+".log", "w") as config_file:
            config_file.write(output)
    except:
        print("SOMETHING WENT WRONG CREATING THE FILE")