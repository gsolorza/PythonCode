import textfsm
from textfsm import clitable
from netmiko.utilities import clitable_to_dict
from pprint import pprint
import io
# Sample data to be parsed

index_file = 'index'
template_dir = '/Users/georgesolorzano/Google Drive/PythonCode/wsl/ntc-templates/ntc_templates/templates'

regex = """
Value INTERFACE (\S+)
Value IP_ADDRESS (\S+)
Value OK (\w+)
Value METHOD (\w+)
Value STATUS (\w+)
Value PROTOCOL (\w+)

Start
  ^\s*Interface.*Status\s+Protocol.* -> Data

Data
  ^${INTERFACE}\s+${IP_ADDRESS}\s+${OK}\s+${METHOD}\s+${STATUS}\s+${PROTOCOL}.* -> Record

"""

cli_table = clitable.CliTable(index_file, template_dir)
attrs = {'Command': "show ip int brief", 'Platform': "cisco_ios"}

template = io.StringIO(regex)

data = """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0/0   74.219.116.162  YES NVRAM  up                    up      
GigabitEthernet0/0/1   unassigned      YES DHCP   administratively down down    
GigabitEthernet0/1/0   unassigned      YES unset  up                    up      
GigabitEthernet0/1/1   unassigned      YES unset  down                  down    
GigabitEthernet0/1/2   unassigned      YES unset  down                  down    
GigabitEthernet0/1/3   unassigned      YES unset  down                  down    
GigabitEthernet0/1/4   unassigned      YES unset  down                  down    
GigabitEthernet0/1/5   unassigned      YES unset  down                  down    
GigabitEthernet0/1/6   unassigned      YES unset  down                  down    
GigabitEthernet0/1/7   unassigned      YES unset  down                  down    
Loopback47233          10.253.8.168    YES NVRAM  up                    up      
Tunnel11               10.253.2.171    YES NVRAM  up                    up      
Tunnel13               10.253.0.121    YES NVRAM  up                    down    
Vlan1                  10.193.10.1     YES NVRAM  up                    up
"""

print(cli_table.ParseCmd(data, attrs))

# Convert from clitable format to list-dict format
structured_data = clitable_to_dict(cli_table)
pprint(structured_data)
# Parse the data using the template
with open("showipinterbrief.template") as template:
    print(template)
    template_obj = textfsm.TextFSM(template)
    
    result = template_obj.ParseText(data)

    # Print the parsed result
    pprint(result)
    print(type(result))