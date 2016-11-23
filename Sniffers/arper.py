__author__ = 'Christian Urcuqui'


# ARP poisoning with Scapy

from scapy.all import *
import os, sys, threading, signal

interface = "en1"
target_ip = ""
gateway_ip = ""
packet_count = 1000

# set the interface
conf.iface = interface

# turn off output
conf.verb = 0

print("[*] Setting up %s" % interface)


# ---------< ---->
# methods to support

def get_mac(ip_address):

    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff:")/ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s,r in responses:
        return r[Ether].src
    return None
























# ---------< ---->

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting.")
    sys.exit(0)
else:
    print("[*] Gateway %s is at %s" % (gateway_ip, gateway_mac))



