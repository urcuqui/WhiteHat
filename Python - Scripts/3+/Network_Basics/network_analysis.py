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

# global variables
windows = False


def settings():

    if os.name == 'nt':
        windows = True
    else:
        windows = False


def main():
    settings()
    nic_available()


def nic_available():
    if windows:
        IFACES.show(True)
    else:
        for e in netifaces.interfaces():
            print(e)


if __name__ == "__main__":
   main()