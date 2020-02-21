#!/usr/bin/env python3

def get_config(connection):
    output = connection.send_command("show running-config")
    hostname = str()
    for line in output.split("\n"):
        if "hostname" in line:
            hostname = line.strip("hostname ")
            break
    print(hostname)
    try:
        with open(hostname+".log", "w") as config_file:
            config_file.write(output)
    except:
        print("SOMETHING WENT WRONG CREATING THE FILE")