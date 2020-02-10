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

resource = "ers/config/guestuser/"

guest_user = {
  "GuestUser" : {
    "name" : "",
    "guestType" : "",
    "guestInfo" : {
      "userName" : "",
      "lastName" : "",
      "password" : ""
    },
    "guestAccessInfo" : {
      "validDays" : 365,
      "location" : ""
    },
    "portalId" : ""
  }
}

def create_guest_user(guest_user):
  r = requests.post(url+resource, headers={"content-type":"application/json", "Accept":"application/json"}, auth=(ise_username, ise_password), verify=False, data=json.dumps(guest_user))
  if r.status_code == 400:
    pprint(r.json()["ERSResponse"]["messages"])
  elif r.status_code == 401:
    print("VALIDATE USERNAME AND PASSWORD")
  elif r.status_code == 201:
    print("USER CREATED")
    print(tabulate(guest_user["GuestUser"]["guestInfo"].items(), tablefmt="fancy_grid"))
  else:
    print (r.status_code)
  
csv_file = csv.DictReader(open("guest_users.csv"))

for row in csv_file:
  guest_user["GuestUser"]["name"] = row["name"]
  guest_user["GuestUser"]["guestType"] = row["guest-type"]
  guest_user["GuestUser"]["guestInfo"]["userName"] = row["username"]
  guest_user["GuestUser"]["guestInfo"]["lastName"] = row["lastname"]
  guest_user["GuestUser"]["guestInfo"]["password"] = row["password"]
  guest_user["GuestUser"]["guestAccessInfo"]["location"] = row["location"]
  guest_user["GuestUser"]["portalId"] = row["portal-id"]
  create_guest_user(guest_user)



