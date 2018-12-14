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
import pyshark  # wrapper
import subprocess
import re

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
    capture_time = input("Write the time in seconds:\n")
    name_packet = input("Write the name of the packet file to save:\n")
    sniffer(interface, capture_time, name_packet)


def sniffer(interface, timeout, name_packet):
    global windows
    if windows:
        print("sniffing...")
        sniff(iface=interface, prn=pkt_callback, store=0)
    else:
        # Linux -> Tcpdump
        print("sniffing...")
        cmd = "tcpdump -G " + timeout + " -W 1 -w " + \
              name_packet + ".pcap -i " + interface
        subprocess.call(cmd, shell=True)


        #capture = pyshark.LiveCapture(interface=interface)
        #capture.sniff(timeout=int(timeout))
        #print(capture)


def pkt_callback(pkt):
            pkt.show() # debug statement


if __name__ == "__main__":
   main()
