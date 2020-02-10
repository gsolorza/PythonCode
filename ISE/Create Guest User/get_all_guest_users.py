#! /usr/bin/env python3

import requests
import json
import sys
from pprint import pprint
import csv
from tqdm import tqdm
from tabulate import tabulate
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ise_ip, ise_username, ise_password  = sys.argv[1], sys.argv[2], sys.argv[3]

url = "https://{}:9060/".format(ise_ip)

resource_get_all_guest_users = "ers/config/guestuser"
resource_get_guest_users_byname = "ers/config/guestuser/name/"

def get_guest_users(resource):
  r = requests.get(url+resource, headers={"content-type":"application/json", "Accept":"application/json"}, auth=(ise_username, ise_password), verify=False)
  if r.status_code == 400:
    pprint(r.json()["ERSResponse"]["messages"])
  elif r.status_code == 401:
    print("VALIDATE USERNAME AND PASSWORD")
  elif r.status_code == 200:
    return json.loads(r.text)
  else:
    print (r.status_code)

guest_users = get_guest_users(resource_get_all_guest_users)

for guest in guest_users["SearchResult"]["resources"]:
    user = get_guest_users(resource_get_guest_users_byname+guest["name"])
    print(tabulate(user["GuestUser"]["guestInfo"].items(), tablefmt="fancy_grid"))







