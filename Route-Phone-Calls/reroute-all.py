import requests
import re
from pprint import pprint
import sys
from tqdm import tqdm

url = "https://api.vitelity.net/api.php?login=netv_api&pass=zPbY9ZjOhCUF&cmd=listdids"

payload = ""
headers = {
  'Cookie': '__cf_bm=u998YoAteHeUvkVYD1Uutfv335X.RN.iOQSI1LCEuGU-1647029415-0-ASAaOTvDjTjJqsS/FDSd0lIdvQZEqejEnob3uAKqdYdBHqsyp5f3jso+d0Yf/8OVuSbZYDlOabNGeHdUW/hyF00='
}


inputUser = sys.argv[1]
inputPwd = sys.argv[2]

rerouteWhere = sys.argv[3] # The value should be the word dc or dr

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


for match in matches:
  ipAddres = match.group(4)
  did = match.group(1)
  if ipAddres == drIpAddress:
    dids['dids']['dr'].append({did:ipAddres})
  elif ipAddres == dcIpAddress:
    dids['dids']['dc'].append({did:ipAddres})
  else:
    pass

dcCount = len(dids['dids']['dc'])
drCount = len(dids['dids']['dr'])

print(f'Total Dids on DR => {drCount}\nTotal Dids on DC =>{dcCount}\n')
answer = input(f'Are you sure to reroute all did numbers to the {rerouteWhere} Cube?\nAnswer: ')


def rerouteNumber(user,pwd,didRecords,ip):
  output = str()
  for record in tqdm(didRecords):
    for did in record.keys():
      rerouteUrl = f'https://api.vitelity.net/api.php?login={user}&pass={pwd}&cmd=reroute&routesip={ip}&did={did}'
      try:
        requests.request("POST", rerouteUrl, headers=headers, data=payload)
        output = (f'Rerouted Did {did} ==> {ip}\n')
      except Exception:
        print("SOMETHING WENT WRONG")
  return output

if answer == 'yes' or answer == 'y':
  if rerouteWhere == 'dc':
    records = dids['dids']['dr']
    result = rerouteNumber(inputUser,inputPwd,records,dcIpAddress)
  elif rerouteWhere == 'dr':
    records = dids['dids']['dc']
    result = rerouteNumber(inputUser,inputPwd,records,drIpAddress)
else:
  sys.exit()


with open('reroute-report.txt', 'w+') as f:
  f.write(result)
