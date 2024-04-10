#!/usr/bin/env python3
import requests
from pprint import pprint
import json

username, password, vmanageIp = "admin", "admin", "vmanage-1045891.viptela.net"
login_data = {
    'j_username' : username, 
    'j_password' : password
    }

baseUrl = f"https://{vmanageIp}"
# resource = "/dataservice/device"
# resource = "/dataservice/device/bfd/sites/detail?state=siteup"
resource = "/dataservice/vedgeinventory/summary"

inventoryControllers = "/dataservice/system/device/controllers"

# query = {
#   "size": 100,                        
#   "query": {
#     "condition": "AND",                 
#     "rules": [
#       {
#         "value": [                     
#           "24"
#         ],
#         "field": "entry_time",
#         "type": "date",
#         "operator": "last_n_hours"
#       }
#     ]
#   }
# }

# params = {
#     "startDate": "2020-07-01T00:00:00",
#     "endDate": "2020-07-010T11:00:00"
# }

session = requests.session()

auth = session.post(baseUrl+"/j_security_check", data=login_data, verify=False)
print(auth.ok)
print(auth.status_code)

response = session.get(baseUrl+resource, verify=False)
print(response.url)
print(response.status_code)
pprint(response.json())

