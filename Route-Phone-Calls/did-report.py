import requests
import json
import re
from pprint import pprint

url = "https://api.vitelity.net/api.php?login=netv_api&pass=zPbY9ZjOhCUF&cmd=listdids"

payload = ""
headers = {
  'Cookie': '__cf_bm=u998YoAteHeUvkVYD1Uutfv335X.RN.iOQSI1LCEuGU-1647029415-0-ASAaOTvDjTjJqsS/FDSd0lIdvQZEqejEnob3uAKqdYdBHqsyp5f3jso+d0Yf/8OVuSbZYDlOabNGeHdUW/hyF00='
}

dcIpAddress='173.252.189.180'
drIpAddress='12.35.51.12'

dids = {'dids':
{'dc': [],
'dr': [],
}}

response = requests.request("POST", url, headers=headers, data=payload)
data = response.text

def find_re(regex, data):
    pattern = re.compile(regex, re.M|re.I)
    return pattern.finditer(data)

matches = find_re(r'(\d+),(.+),(.+),(.+)', data)

with open('did-report.txt', 'w+') as f:
  for match in matches:
    ipAddres = match.group(4)
    did = match.group(1)
    if ipAddres == drIpAddress:
      dids['dids']['dr'].append({did:ipAddres})
      f.write(f'DR -> {did} -> {drIpAddress}\n')
    elif ipAddres == dcIpAddress:
      dids['dids']['dc'].append({did:ipAddres})
      f.write(f'DC -> {did} -> {dcIpAddress}\n')
    else:
      pass



# def rerouteNumber(user,pwd,did,ip):
#   rerouteUrl = f'https://api.vitelity.net/api.php?login={user}&pass={pwd}&cmd=reroute&routesip={ip}&did={did}'
#   response = requests.request("POST", url, headers=headers, data=payload)

# dcCount = len(dids['dids']['dc'])
# drCount = len(dids['dids']['dr'])

# print(drCount, dcCount)