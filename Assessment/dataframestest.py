#!/usr/bin/env python3

import pandas as pd
import json
from pprint import pprint

devices_data = [{'gnan02-3560sw-pr': [{'show_version': '{"version": "12.2(55)SE3", "rommon": '
                                        '"Bootstrap", "hostname": '
                                        '"gnan02-3560sw-pr", "uptime": "50 '
                                        'weeks, 18 hours, 40 minutes", '
                                        '"reload_reason": "power-on", '
                                        '"running_image": '
                                        '"/c3560e-universalk9-mz.122-55.SE3/c3560e-universalk9-mz.122-55.SE3.bin", '
                                        '"hardware": ["WS-C3560X-24"], '
                                        '"serial": ["FDO1536R1V9"], '
                                        '"config_register": "0xF", "mac": '
                                        '["CC:EF:48:DA:20:00"]}'},
                       {'show_clock': '{"time": "19:09:23.965", "timezone": '
                                      '"CL", "dayweek": "Thu", "month": "Mar", '
                                      '"day": "5", "year": "2020"}'}]},
 {'gnan12-2960sw-pr': [{'show_version': '{"version": "12.2(44)SE6", "rommon": '
                                        '"Bootstrap", "hostname": '
                                        '"gnan12-2960sw-pr", "uptime": "5 '
                                        'years, 14 weeks, 5 days, 8 hours, 37 '
                                        'minutes", "reload_reason": '
                                        '"power-on", "running_image": '
                                        '"c2960-lanbasek9-mz.122-44.SE6/c2960-lanbasek9-mz.122-44.SE6.bin", '
                                        '"hardware": ["WS-C2960-24PC-L"], '
                                        '"serial": ["FOC1421Z2QK"], '
                                        '"config_register": "0xF", "mac": '
                                        '["A8:B1:D4:06:11:80"]}'},
                       {'show_clock': '{"time": "19:09:18.557", "timezone": '
                                      '"CL", "dayweek": "Thu", "month": "Mar", '
                                      '"day": "5", "year": "2020"}'}]},
 {'RTR_ANGAMOS01': [{'show_version': '{"version": "15.4(3)M3", "rommon": '
                                     '"System", "hostname": "RTR_ANGAMOS01", '
                                     '"uptime": "49 weeks, 2 days, 6 hours, 30 '
                                     'minutes", "reload_reason": "power-on", '
                                     '"running_image": '
                                     '"c3900-universalk9-mz.SPA.154-3.M3.bin", '
                                     '"hardware": ["CISCO3925-CHASSIS"], '
                                     '"serial": ["FJC2028D155"], '
                                     '"config_register": "0x2102", "mac": []}'},
                    {'show_clock': '{"time": "19:09:38.401", "timezone": '
                                   '"Stgo", "dayweek": "Thu", "month": "Mar", '
                                   '"day": "5", "year": "2020"}'}]},
 {'sw-ang-Sala.Ctrl': [{'show_version': '{"version": "15.2(2)E6", "rommon": '
                                        '"Bootstrap", "hostname": '
                                        '"sw-ang-Sala.Ctrl", "uptime": "2 '
                                        'years, 15 weeks, 5 days, 9 hours, 21 '
                                        'minutes", "reload_reason": '
                                        '"power-on", "running_image": '
                                        '"/c2960-lanbasek9-mz.152-2.E6/c2960-lanbasek9-mz.152-2.E6.bin", '
                                        '"hardware": ["WS-C2960+24PC-L"], '
                                        '"serial": ["FOC2117Y2SF"], '
                                        '"config_register": "0xF", "mac": '
                                        '["00:A3:D1:E2:06:80"]}'},
                       {'show_clock': '{"time": "19:11:04.513", "timezone": '
                                      '"CL", "dayweek": "Thu", "month": "Mar", '
                                      '"day": "5", "year": "2020"}'}]},
 {'gnan10-3560sw-pr': [{'show_version': '{"version": "12.2(50)SE5", "rommon": '
                                        '"Bootstrap", "hostname": '
                                        '"gnan10-3560sw-pr", "uptime": "14 '
                                        'weeks, 2 hours, 48 minutes", '
                                        '"reload_reason": "power-on", '
                                        '"running_image": '
                                        '"/c3560-ipbasek9-mz.122-50.SE5/c3560-ipbasek9-mz.122-50.SE5.bin", '
                                        '"hardware": ["WS-C3560V2-24TS"], '
                                        '"serial": ["FDO1518X1TS"], '
                                        '"config_register": "0xF", "mac": '
                                        '["E8:BA:70:CB:B2:80"]}'},
                       {'show_clock': '{"time": "19:09:53.954", "timezone": '
                                      '"CL", "dayweek": "Thu", "month": "Mar", '
                                      '"day": "5", "year": "2020"}'}]}]


result = {
    "device_name": []
}


for device in devices_data:
    for hostname, device_data in device.items():
        result["device_name"].append(hostname)
        for data in device_data:
            for command, output in data.items():
                for key, value in json.loads(output).items():
                    try:
                        result[key].append(value)
                    except KeyError:
                        result[key] = []
                        result[key].append(value)

                    
df = pd.DataFrame(result)
print(df)

