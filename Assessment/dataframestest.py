#!/usr/bin/env python3

import pandas as pd
import json
from pprint import pprint
import os

def dataframe(data):
    dataframes = {}
    for device in data:
        for hostname, device_data in device.items():
            dataframes[hostname] =  []
            for data in device_data:
                for command, output in data.items():
                    df = {}          
                    try:        
                        for item in output:
                            for key, value in item.items():
                                try:
                                    df[key].append(value)
                                except KeyError:
                                    df[key] = []
                                    df[key].append(value)
                        dataframes[hostname].append({command: df})
                    except:
                        continue
    return dataframes
