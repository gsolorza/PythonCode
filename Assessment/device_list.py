import csv
from netmiko import ConnectHandler

def unpack_device_list():
    with open("device_list.csv") as file:
        devices = csv.DictReader(file)
        device_list = [dev for dev in devices]
        return device_list
    