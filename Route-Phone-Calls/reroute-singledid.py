import requests
from pprint import pprint
import sys

payload = ""
headers = {
  'Cookie': '__cf_bm=u998YoAteHeUvkVYD1Uutfv335X.RN.iOQSI1LCEuGU-1647029415-0-ASAaOTvDjTjJqsS/FDSd0lIdvQZEqejEnob3uAKqdYdBHqsyp5f3jso+d0Yf/8OVuSbZYDlOabNGeHdUW/hyF00='
}

inputUser = sys.argv[1]
inputPwd = sys.argv[2]
inputdid = sys.argv[3]
inputIp = sys.argv[4]

dcIpAddress='173.252.189.180'
drIpAddress='12.35.51.12'

def rerouteNumber(user,pwd,did,ip):
  rerouteUrl = f'https://api.vitelity.net/api.php?login={user}&pass={pwd}&cmd=reroute&routesip={ip}&did={did}'
  try:
    requests.request("POST", rerouteUrl, headers=headers, data=payload)
    print(f'Rerouted Did {did} ==> {ip}\n')
  except Exception:
    print("SOMETHING WENT WRONG")

rerouteNumber(inputUser,inputPwd,inputdid,inputIp)