#!/usr/bin/env python3

from netmiko import ConnectHandler
import sys

class Connect_Manager():

    @staticmethod
    def connect(**device):
        try:
            return ConnectHandler(**device)
        except Exception as failure:
            print("THERE WAS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <--".format(failure))


