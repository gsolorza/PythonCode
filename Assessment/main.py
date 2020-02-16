#!/usr/bin/env python3

from netmiko import ConnectHandler
from napalm import get_network_driver
from pprint import pprint

# driver = get_network_driver('ios')

# device = driver("10.100.1.82", "cisco", "cisco")
# device.open()

# pprint(device.get_interfaces_counters())

cisco = {
    "device_type": "cisco_ios",
    "host": "10.100.1.82",
    "username": "cisco",
    "password": "cisco"
}

c = ConnectHandler(**cisco)


