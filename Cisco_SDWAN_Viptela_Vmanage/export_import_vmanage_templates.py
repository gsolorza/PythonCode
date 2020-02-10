#!/usr/bin/env python3

"""
Class with REST Api GET and POST libraries

Example: python rest_api_lib.py vmanage_hostname username password

PARAMETERS:
    vmanage_hostname : Ip address of the vmanage or the dns name of the vmanage
    username : Username to login the vmanage
    password : Password to login the vmanage
    action : export|import templates

Note: All the three arguments are manadatory
"""
import requests
import sys
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import os
from tqdm import tqdm
from tabulate import tabulate

def readable_json(data):
    print (json.dumps(data, indent=2))

def create_file(name, data):
    with open(name, "w+") as json_file:
        json.dump(data, json_file)

class rest_api_lib:
    def __init__(self, vmanage_ip, username, password):
        self.vmanage_ip = vmanage_ip
        self.session = {}
        self.login(self.vmanage_ip, username, password)

    def login(self, vmanage_ip, username, password):
        """Login to vmanage"""
        base_url_str = 'https://%s/'%vmanage_ip

        login_action = '/j_security_check'

        #Format data for loginForm
        login_data = {'j_username' : username, 'j_password' : password}

        #Url for posting login data
        login_url = base_url_str + login_action

        url = base_url_str + login_url

        sess = requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = sess.post(url=login_url, data=login_data, verify=False)

        if "<html>" in login_response.content.decode(("utf-8")):
            print ("Login Failed")
            sys.exit(0)

        self.session[vmanage_ip] = sess

    def get_request(self, mount_point):
        """GET request"""
        url = "https://%s:8443/dataservice/%s"%(self.vmanage_ip, mount_point)
        # print (url)
        response = self.session[self.vmanage_ip].get(url, verify=False)
        data = response.json()
        return data

    def post_request(self, mount_point, payload, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:8443/dataservice/%s"%(self.vmanage_ip, mount_point)
        response = self.session[self.vmanage_ip].post(url=url, data=payload, headers=headers, verify=False)
        data = response.content
        return data
    
    def delete_request(self, mount_point, headers={'Content-Type': 'application/json'}):
        """POST request"""
        url = "https://%s:8443/dataservice/%s"%(self.vmanage_ip, mount_point)
        response = self.session[self.vmanage_ip].delete(url=url, headers=headers, verify=False)
        data = response.content
        return data
        
def main(args):
    if not len(args) == 4:
        print (__doc__)
        return
    vmanage_ip, username, password, action = args[0], args[1], args[2], args[3]

    obj = rest_api_lib(vmanage_ip, username, password)    
    inventory = {"Template Name":[], "Device Type":[]}
    
    if action == "export":
        try:
            os.mkdir("backup_vmanage_templates")
        except FileExistsError:
            pass
        os.chdir("backup_vmanage_templates")
        response = obj.get_request('template/feature')
        for item in tqdm(response["data"], ascii=True):
            if item["factoryDefault"] == False:
                inventory["Template Name"].append(item["templateName"])
                inventory["Device Type"].append([x for x in item["deviceType"]])
                response = obj.get_request('template/feature/object/'+item["templateId"])
                create_file(item["templateName"], json.dumps(response))
        print("EXPORT COMPLETED CHECK: 'backup_vmanage_templates' FOLDER")
        print(tabulate(inventory, headers="keys", tablefmt="fancy_grid"))

    elif action == "import":
        os.chdir("backup_vmanage_templates")
        for backup in tqdm(os.listdir("."), ascii=True):
            with open(backup, "r") as json_file:
                template = json.load(json_file)
                response = obj.post_request("template/feature", template)
        print("IMPORT COMPLETED CHECK ON VMANAGE")
    # elif action == "delete":
    #     os.chdir("backup_vmanage_templates")
    #     for backup in tqdm(os.listdir("."), ascii=True):
    #         with open(backup, "r") as json_file:
    #             payload = json.load(json_file) 
    #             template = json.loads(payload)
    #             response = obj.delete_request("template/feature/"+template["templateId"])

 ## Backup process             
 ## 1. GET --> template/feature/object/831c8b04-69a7-461a-9f17-02c23ff017d3 --> take the config from the template in json format
 ## 2. POST --> template/feature --> post the config taken in the previous get       

#Example request to make a Post call to the vmanage "url=https://vmanage.viptela.com/dataservice/device/action/rediscover"
# payload = {"action":"rediscover","devices":[{"deviceIP":"172.16.248.105"},{"deviceIP":"172.16.248.106"}]}
# response = obj.post_request('device/action/rediscover', payload)
# print response

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))