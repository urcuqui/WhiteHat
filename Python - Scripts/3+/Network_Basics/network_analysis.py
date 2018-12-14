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


def settings():

    if os.name == 'nt':
        print("ok")
    else:
        print("nada")


def main():
    settings()
    #nic_available()


def nic_available():
    show_interfaces()


    #for interface in get_windows_if_list():
    #   print(interface)

if __name__ == "__main__":
   #main()
   IFACES.show(True)