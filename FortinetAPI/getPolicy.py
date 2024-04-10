import requests
import json
from pprint import pprint
import time
import sys
import urllib3
import pandas as pd
import os
from tqdm import tqdm

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
    if "syslog" in deviceName.lower():
      continue
    elif "es-cor-ft1" in deviceName.lower():
      continue
    deviceIpAddress = device["ip"]
    deviceInfo = {"name": deviceName, "ipAddress": deviceIpAddress}
    deviceList.append(deviceInfo)

  return deviceList

managerDevList = GetDeviceList("10.130.175.5")

writer = pd.ExcelWriter("policy.xlsx", engine="xlsxwriter")

for device in tqdm(managerDevList, ascii=True):
  deviceIP = device["ipAddress"]
  deviceName = device["name"]
  policyIdList = []
  policyName = []
  serviceList = []
  srcAddrList = []
  dstAddrList = []
  srcIntList = []
  dstIntrList = []
  appProfileList = []
  avProfileList = []
  webProfileList = []
  dnsProfileList = []
  dataFrame = {
      "Policy ID": policyIdList,
      "Policy Name": policyName,
      "Source Int List": srcIntList,
      "Destination Int List": dstIntrList,
      "Source Address": srcAddrList,
      "Destination Address": dstAddrList,
      "Service": serviceList,
      "Application Profile": appProfileList,
      "AV Profile": avProfileList,
      "Web Profile": webProfileList,
      "DNS Profile": dnsProfileList
  }

  urlAuth = f"https://{deviceIP}/logincheck"
  urlPolicy = f"https://{deviceIP}/api/v2/cmdb/firewall/policy/"
  payload = "username=admin&secretkey=p6pY3QEWvs1!2H3aWiyP"

  try:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()
    auth = session.post(urlAuth, data=payload, verify=False)
    cookies = auth.cookies
    cookies_dict = requests.utils.dict_from_cookiejar(cookies)
    csrftoken = eval(cookies_dict["ccsrftoken"])
    headers = auth.headers
    headers["X-CSRFToken"] = csrftoken
    headers["Content-Type"] = 'text/plain'
    policy = session.get(urlPolicy, headers=headers, verify=False)
  except Exception:
    print(f"Error Connecting to Device {deviceName}\n")
    continue

  json1 = json.loads(policy.text).get("results")
  session.close()
  
  def decapsulateData(data):
    output = ""

    if isinstance(data, list):
      for item in data:
        output += item["name"]+"\n"
      return output
    elif isinstance(data, str):
      if data:
        return data
      else:
        return "None"
    elif isinstance(data, int):
      return data

  for policy in json1:
    id = decapsulateData(policy["policyid"])
    name = decapsulateData(policy["name"])
    appProfile = decapsulateData(policy["application-list"])
    avProfile = decapsulateData(policy["av-profile"])
    webProfile = decapsulateData(policy["webfilter-profile"])
    dnsProfile = decapsulateData(policy["dnsfilter-profile"])
    service = decapsulateData(policy["service"])
    srcAddr = decapsulateData(policy["srcaddr"])
    srcInt = decapsulateData(policy["srcintf"])
    dstAddr = decapsulateData(policy["dstaddr"])
    dstInt = decapsulateData(policy["dstintf"])
    policyIdList.append(id)
    policyName.append(name)
    serviceList.append(service)
    srcAddrList.append(srcAddr)
    srcIntList.append(srcInt)
    dstAddrList.append(dstAddr)
    dstIntrList.append(dstInt)
    appProfileList.append(appProfile)
    avProfileList.append(avProfile)
    webProfileList.append(webProfile)
    dnsProfileList.append(dnsProfile)

  print(os.getcwd())
  df = pd.DataFrame(dataFrame)
  df.to_excel(writer, deviceName)

writer.save()

"""
{'action': 'accept',
 'anti-replay': 'enable',
 'application-list': 'block-high-risk',
 'auth-cert': '',
 'auth-path': 'disable',
 'auth-redirect-addr': '',
 'auto-asic-offload': 'enable',
 'av-profile': 'default',
 'block-notification': 'disable',
 'captive-portal-exempt': 'disable',
 'capture-packet': 'disable',
 'cifs-profile': '',
 'comments': '',
 'custom-log-fields': [],
 'decrypted-traffic-mirror': '',
 'delay-tcp-npu-session': 'disable',
 'diffserv-forward': 'disable',
 'diffserv-reverse': 'disable',
 'diffservcode-forward': '000000',
 'diffservcode-rev': '000000',
 'disclaimer': 'disable',
 'dlp-sensor': '',
 'dnsfilter-profile': '',
 'dsri': 'disable',
 'dstaddr': [{'name': 'all', 'q_origin_key': 'all'}],
 'dstaddr-negate': 'disable',
 'dstaddr6': [],
 'dstintf': [{'name': 'wan1', 'q_origin_key': 'wan1'},
             {'name': 'wan2', 'q_origin_key': 'wan2'}],
 'dynamic-shaping': 'disable',
 'email-collect': 'disable',
 'emailfilter-profile': '',
 'fec': 'disable',
 'file-filter-profile': '',
 'firewall-session-dirty': 'check-all',
 'fixedport': 'disable',
 'fsso-agent-for-ntlm': '',
 'fsso-groups': [],
 'geoip-anycast': 'disable',
 'geoip-match': 'physical-location',
 'global-label': '',
 'groups': [],
 'http-policy-redirect': 'disable',
 'icap-profile': '',
 'identity-based-route': '',
 'inbound': 'disable',
 'inspection-mode': 'proxy',
 'internet-service': 'disable',
 'internet-service-custom': [],
 'internet-service-custom-group': [],
 'internet-service-group': [],
 'internet-service-name': [],
 'internet-service-negate': 'disable',
 'internet-service-src': 'disable',
 'internet-service-src-custom': [],
 'internet-service-src-custom-group': [],
 'internet-service-src-group': [],
 'internet-service-src-name': [],
 'internet-service-src-negate': 'disable',
 'ippool': 'disable',
 'ips-sensor': 'default',
 'label': '',
 'logtraffic': 'all',
 'logtraffic-start': 'disable',
 'match-vip': 'disable',
 'match-vip-only': 'disable',
 'name': 'Global-policies--->>ASB-DAL-FAR_  7',
 'nat': 'enable',
 'nat46': 'disable',
 'nat64': 'disable',
 'natinbound': 'disable',
 'natip': '0.0.0.0 0.0.0.0',
 'natoutbound': 'disable',
 'np-acceleration': 'enable',
 'ntlm': 'disable',
 'ntlm-enabled-browsers': [],
 'ntlm-guest': 'disable',
 'outbound': 'enable',
 'passive-wan-health-measurement': 'disable',
 'per-ip-shaper': '',
 'permit-any-host': 'disable',
 'permit-stun-host': 'disable',
 'policyid': 1071741878,
 'poolname': [],
 'poolname6': [],
 'profile-group': '',
 'profile-protocol-options': 'default',
 'profile-type': 'single',
 'q_origin_key': 1071741878,
 'radius-mac-auth-bypass': 'disable',
 'redirect-url': '',
 'replacemsg-override-group': '',
 'reputation-direction': 'destination',
 'reputation-minimum': 0,
 'rtp-addr': [],
 'rtp-nat': 'disable',
 'schedule': 'always',
 'schedule-timeout': 'disable',
 'sctp-filter-profile': '',
 'send-deny-packet': 'disable',
 'service': [{'name': 'ALL', 'q_origin_key': 'ALL'}],
 'service-negate': 'disable',
 'session-ttl': '0',
 'sgt': [],
 'sgt-check': 'disable',
 'src-vendor-mac': [],
 'srcaddr': [{'name': 'all', 'q_origin_key': 'all'}],
 'srcaddr-negate': 'disable',
 'srcaddr6': [],
 'srcintf': [{'name': 'VLAN100', 'q_origin_key': 'VLAN100'},
             {'name': 'VLAN200', 'q_origin_key': 'VLAN200'},
             {'name': 'VLAN777', 'q_origin_key': 'VLAN777'}],
 'ssh-filter-profile': '',
 'ssh-policy-redirect': 'disable',
 'ssl-ssh-profile': 'Clone of no-inspection',
 'status': 'enable',
 'tcp-mss-receiver': 0,
 'tcp-mss-sender': 0,
 'tcp-session-without-syn': 'disable',
 'timeout-send-rst': 'disable',
 'tos': '0x00',
 'tos-mask': '0x00',
 'tos-negate': 'disable',
 'traffic-shaper': '',
 'traffic-shaper-reverse': '',
 'users': [],
 'utm-status': 'enable',
 'uuid': '2fdff024-fd40-51ec-c81e-4a27bf2801a0',
 'uuid-idx': 522,
 'videofilter-profile': '',
 'vlan-cos-fwd': 255,
 'vlan-cos-rev': 255,
 'vlan-filter': '',
 'voip-profile': '',
 'vpntunnel': '',
 'waf-profile': '',
 'wanopt': 'disable',
 'wanopt-detection': 'active',
 'wanopt-passive-opt': 'default',
 'wanopt-peer': '',
 'wanopt-profile': '',
 'wccp': 'disable',
 'webcache': 'disable',
 'webcache-https': 'disable',
 'webfilter-profile': 'Custom WF and DBL',
 'webproxy-forward-server': '',
 'webproxy-profile': '',
 'ztna-ems-tag': [],
 'ztna-geo-tag': [],
 'ztna-status': 'disable'}


"""