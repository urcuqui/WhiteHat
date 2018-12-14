"""
Author: Christian Camilo Urcuqui
Date: 14 december 2018

This solution is only available to capture packages from devices that have windows or linux operative systems
Python version: 3+
"""

# libraries
import netifaces
from scapy.all import *
import os
import pyshark

# global variables
windows = False


def settings():
    global windows
    if os.name == 'nt':
        windows = True
    else:
        windows = False


def main():
    settings()
    nic_treatment()


def nic_treatment():
    global windows
    if windows:
        IFACES.show(True)
    else:
        for e in netifaces.interfaces():
            print(e)
    print(" -------- ")
    text = input("Write the name of the network interface to use:\n")
    sniffer(text)


def sniffer(type_os):
    capture = pyshark.LiveCapture(interface='eth0')
    capture.sniff(timeout=50)
    capture



if __name__ == "__main__":
   main()