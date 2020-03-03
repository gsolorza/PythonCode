#!/usr/bin/env python3

from netmiko import ConnectHandler
import sys

class Connect_Manager():

    def connect(self, **devices):
        try:
            return ConnectHandler(**self.device)
        except Exception as failure:
            print("THERE WAS AN ERROR TRYING TO CONNECT TO THE DEVICE:\n--> {} <--".format(failure))


