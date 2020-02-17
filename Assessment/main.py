#!/usr/bin/env python3

from napalm import get_network_driver
from pprint import pprint

driver = get_network_driver('ios')

device = driver("10.100.1.82", "cisco", "cisco")
device.open()

pprint(device.get_interfaces_counters())


