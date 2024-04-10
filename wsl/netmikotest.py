from netmiko import ConnectHandler
from pprint import pprint

device = { "device_type": "cisco_ios",
    "host" : "10.253.8.168",
    "username": "lairdadmin",
    "password": "WgU0znN(qhxf"}

connection = ConnectHandler(**device)
output_list = connection.send_command("show ip interface brief", use_textfsm=True)
pprint(output_list)
