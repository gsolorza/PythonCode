import requests
import json
from pprint import pprint
import time
import sys

username = sys.argv[1]
password = sys.argv[2]

def GetDeviceInfo(ip, device):
  deviceList = []
  url = f"https://{ip}/jsonrpc"

  payload = json.dumps({
    "id": 1,
    "method": "exec",
    "params": [
      {
        "data": {
          "user": username,
          "passwd": password
        },
        "url": "/sys/login/user"
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  session = response.json()["session"]
  del response
  del payload
  pprint(session)

  payload = json.dumps({
    "method": "get",
    "params": [
      {
        "url": f"/dvmdb/device/{device}"
      }
    ],
    "session": session,
    "verbose": 1,
    "id": 1
  })

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  data = response.json()["result"][0]["data"]
  deviceVersion = data["os_ver"]
  devicePatch = data["patch"]
  deviceData = {"version": deviceVersion, "Patch": devicePatch}
  return deviceData

#########

def GetDeviceList(ip):
  deviceList = []
  url = f"https://{ip}/jsonrpc"

  payload = json.dumps({
    "id": 1,
    "method": "exec",
    "params": [
      {
        "data": {
          "user": "admin",
          "passwd": "p6pY3QEWvs1!2H3aWiyP"
        },
        "url": "/sys/login/user"
      }
    ]
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  session = response.json()["session"]
  del response
  del payload
  pprint(session)

  payload = json.dumps({
    "method": "get",
    "params": [
      {
        "url": "/dvmdb/device"
      }
    ],
    "session": session,
    "verbose": 1,
    "id": 1
  })

  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  deviceData = response.json()["result"][0]["data"]

  for device in deviceData:
    deviceName = device["name"]
    deviceList.append(deviceName)

  return deviceList

managerDevList = GetDeviceList("10.130.175.4")
analyzerDevList = GetDeviceList("10.130.175.5")

managerDevTotal = len(managerDevList)
analyzerDevTotal = len(analyzerDevList)
print(f"FortiManager has {managerDevTotal} devices")
print(f"FortiAnalyzer has {analyzerDevTotal} devices")

notInFM = []
notInFA = []

# for device in notInFM:
#   print(device)
  # deviceData = GetDeviceInfo("10.130.175.5", "3PH-CHI-FNGW1")
  # print(f"{device} -> {deviceData}")



if sys.argv[3]:
  siteName = sys.argv[1]
  deviceData = GetDeviceInfo("10.130.175.5", siteName)
  print(f"{siteName} -> {deviceData}")

else:
  for analyzerdev in analyzerDevList:
    if analyzerdev not in managerDevList:
      notInFM.append(analyzerdev)
  
  for managerdev in managerDevList:
    if managerdev not in analyzerDevList:
      notInFA.append(managerdev)

  pprint(notInFM)
  print("#"*100+"\n")
  pprint(notInFA)

"""
Output device sample
{'adm_pass': ['ENC',
              'I7MGNDsb7wnBiPPpr4YTtlsbnWxiyYVnMTAx3NgMBDmWfVWE/d2yNbZTugtRjLogCaCXdZbqUqnaplkaOMQJ807wO1yTBD0RBEJZlKdQkRBItgJdGkgSidUKhH6FbnNX8GwTstCYy3JgMJ+iBMYhUwplvzFA9AIFKyPFs2tMpoByw53Y'],
 'adm_usr': '',
 'app_ver': '',
 'av_ver': '',
 'beta': -1,
 'branch_pt': 296,
 'build': 366,
 'checksum': '',
 'conf_status': 'unknown',
 'conn_mode': 'active',
 'conn_status': 'UNKNOWN',
 'db_status': 'unknown',
 'desc': 'Model device',
 'dev_status': 'unknown',
 'fap_cnt': 0,
 'faz.full_act': 0,
 'faz.perm': 15,
 'faz.quota': 0,
 'faz.used': 0,
 'fex_cnt': 0,
 'flags': ['has_hdd', 'is_model', 'linked_to_model'],
 'foslic_cpu': 0,
 'foslic_dr_site': 'disable',
 'foslic_inst_time': 0,
 'foslic_last_sync': 0,
 'foslic_ram': 0,
 'foslic_type': 'temporary',
 'foslic_utm': None,
 'fsw_cnt': 0,
 'ha_group_id': 0,
 'ha_group_name': '',
 'ha_mode': 'standalone',
 'ha_slave': None,
 'hdisk_size': 0,
 'hostname': '',
 'hw_rev_major': 0,
 'hw_rev_minor': 0,
 'hyperscale': 0,
 'ip': '10.10.53.1',
 'ips_ext': 0,
 'ips_ver': '',
 'last_checked': 0,
 'last_resync': 0,
 'latitude': '0.0',
 'lic_flags': 0,
 'lic_region': '',
 'location_from': '',
 'logdisk_size': 0,
 'longitude': '0.0',
 'maxvdom': 10,
 'mgmt.__data[0]': 0,
 'mgmt.__data[1]': 0,
 'mgmt.__data[2]': 0,
 'mgmt.__data[3]': 0,
 'mgmt.__data[4]': 0,
 'mgmt.__data[5]': 0,
 'mgmt.__data[6]': 0,
 'mgmt.__data[7]': 0,
 'mgmt_id': 1643941875,
 'mgmt_if': '',
 'mgmt_mode': 'faz',
 'mgt_vdom': '',
 'module_sn': '',
 'mr': 0,
 'name': '3PH-BLO-FNGW1',
 'node_flags': 0,
 'nsxt_service_name': None,
 'oid': 3795,
 'opts': 0,
 'os_type': 'fos',
 'os_ver': '7.0',
 'patch': 6,
 'platform_str': 'FortiGate-61F',
 'prefer_img_ver': '',
 'prio': 0,
 'private_key': None,
 'private_key_status': 0,
 'psk': '',
 'role': 'master',
 'sn': 'FGT61FTK20014337',
 'source': None,
 'tab_status': '',
 'tunnel_cookie': '',
 'tunnel_ip': '',
 'vdom': [{'comments': None,
           'devid': '3PH-BLO-FNGW1',
           'ext_flags': 0,
           'flags': None,
           'name': 'root',
           'node_flags': 0,
           'oid': 3,
           'opmode': None,
           'rtm_prof_id': 0,
           'status': None,
           'tab_status': None,
           'vdom_type': None,
           'vpn_id': 0}],
 'version': 700,
 'vm_cpu': 0,
 'vm_cpu_limit': 0,
 'vm_lic_expire': 0,
 'vm_mem': 0,
 'vm_mem_limit': 0,
 'vm_status': 0}

"""