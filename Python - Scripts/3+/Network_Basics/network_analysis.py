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
    print("")
    interface = input("Write the name of the network interface to use:\n")
    time = input("Write the time in seconds:\n")
    sniffer(interface, time)


def sniffer(interface, timeout):
    global windows
    if windows:
        print("nada")
        sniff(iface="<My Interface>", prn=pkt_callback, filter="tcp", store=0)

    else:
        print("sniffing...")
        capture = pyshark.LiveCapture(interface=interface)
        capture.sniff(timeout=int(timeout))
        print(capture)


def pkt_callback(pkt):
            pkt.show() # debug statement


if __name__ == "__main__":
   main()
