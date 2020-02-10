#! /usr/bin/env python3

import requests
import json
import sys
from pprint import pprint
import csv
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from tabulate import tabulate

ise_ip, ise_username, ise_password  = sys.argv[1], sys.argv[2], sys.argv[3]

url = "https://{}:9060/".format(ise_ip)

resource = "ers/config/portal"

def get_sponsor_portal_id():
  r = requests.get(url+resource, headers={"content-type":"application/json", "Accept":"application/json"}, auth=(ise_username, ise_password), verify=False)
  if r.status_code == 400:
    pprint(r.json()["ERSResponse"]["messages"])
  elif r.status_code == 401:
    print("VALIDATE USERNAME AND PASSWORD")
  elif r.status_code == 200:
    return json.loads(r.text)["SearchResult"]["resources"]
  else:
    print (r.status_code)

portal_list = get_sponsor_portal_id()

for portal in portal_list:
  if "sponsor portal" in portal["name"].lower():
    print (tabulate({"Portal ID": portal["id"]}.items(), tablefmt="fancy_grid"))
    


