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
processed_data = {}

def settings():
    global windows
    if os.name == 'nt':
        windows = True
    else:
        windows = False


def capture():
    nic_treatment()


def feature_generator():
    pcap_path = input("Write the path of the pcap to process")
    dataset_path = input("Write the path of the dataset to save")
    dataset = open(dataset_path, "w+")
    capture = pyshark.FileCapture(pcap_path)
    dataset.writelines('SourceIP;DestinationIP;SourcePort;DestinationPort;Flow_protocol\n')
    dataset.writelines(str(features(capture)))


def features(capture):
    print ("################### Writing the data #############################")
    pkts = []
    global processed_data

    for pkt in capture:
        try:
            protocol = pkt.transport_layer
            src_addr = pkt.ip.src
            src_port = pkt[pkt.transport_layer].srcport
            dst_addr = pkt.ip.dst
            dst_port = pkt[pkt.transport_layer].dstport

            # save the data whose are processing in a checklist
            processed_data["protocol"] = pkt.transport_layer
            processed_data["src_addr"] = pkt.ip.src
            processed_data["src_port"] = pkt[pkt.transport_layer].srcport
            processed_data["dst_addr"] = pkt.ip.dst
            processed_data["dst_port"] = pkt[pkt.transport_layer].dstport

            if protocol == 'TCP':
                tcp_flow(capture, src_addr, src_port, dst_addr, dst_port)

        except AttributeError:
            pass
        except Exception:
            print("Error during the pcap process")
    return pkts


def tcp_flow(capture, src_addr, src_port, dst_addr, dst_port):


    duration_flow_first = 0
    duration_flow = 0
    number_bytes_sent_per_flow = 0
    number_bytes_received_per_flow = 0
    total_bytes_headers_forward_direction = 0
    i = 0
    for pkt in capture:
        try:
            if pkt.transport_layer == 'TCP' and pkt.ip.src == src_addr and pkt.ip.dst == dst_addr \
                    and pkt['TCP'].dstport == dst_port and pkt['TCP'].srcport == src_port:

                number_bytes_sent_per_flow = number_bytes_sent_per_flow + pkt.captured_length

                if i == 0:
                    duration_flow_first = pkt.frame_info.time_epoch
                i += 1

                duration_flow = pkt.frame_info.time_epoch - duration_flow_first

                if pkt.transport_layer == 'TCP' and pkt.ip.src == dst_addr and pkt.ip.dst == src_addr \
                    and pkt['TCP'].dstport == dst_port and pkt['TCP'].srcport == src_port:

                    number_bytes_received_per_flow = number_bytes_received_per_flow + pkt.captured_length


        except AttributeError:
            pass
        except Exception:
            print("Error during the pcap process")
    #return numero_puertos



def main():

    settings()
    out = True
    while out:
        options = input("Write the number of the option:\n (1) - Capture the network traffic \n (2) - Dataset generator"
                        "\n (3) - Exit")
        if int(options) == 1:
            capture()
        if int(options) == 2:
            feature_generator()
        if int(options) == 3:
            out = False
            exit(0)


def nic_treatment():
    global windows
    print("These are your Network Interface Cards available:\n")
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


def pkt_callback(pkt):
            pkt.show() # debug statement


if __name__ == "__main__":
   main()
