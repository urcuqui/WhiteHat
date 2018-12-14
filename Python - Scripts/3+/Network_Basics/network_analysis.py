"""
Author: Christian Camilo Urcuqui
Date: 14 december 2018
"""

# libraries
import netifaces
from scapy.all import *

def main():
    nic_available()


def nic_available():
    show_interfaces()


    #for interface in get_windows_if_list():
    #   print(interface)

if __name__ == "__main__":
   #main()
   show_interfaces()