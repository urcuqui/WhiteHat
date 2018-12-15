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

# global variables
windows = False
processed_data = []


def settings():
    """
    the next method allows us to define the settings of the program
    according of the operating the system to analyze
    """
    global windows
    if os.name == 'nt':
        windows = True
    else:
        windows = False


def capture():
    """
    Capture allows us to define the parameters (nic, time and package name) in order to do the capture process
    """
    nic_treatment()
    interface = input("Write the name of the network interface to use:\n")
    capture_time = input("Write the time in seconds:\n")
    name_packet = input("Write the name of the packet file to save:\n")
    sniffer(interface, capture_time, name_packet)


def feature_generator():
    """
    This method is dedicated to get all the features from the pcap and makes the dataset
    """
    pcap_path = input("Write the path of the pcap to process")
    dataset_path = input("Write the path of the dataset to save")
    dataset = open(dataset_path, "w+")
    capture = pyshark.FileCapture(pcap_path)
    dataset.writelines('source_ip;destination_ip;source_port;destination_port;flow_protocol;'
                       'duration_of_the_flow;number_of_bytes_sent_per_flow;number_of_bytes_received_per_flow;'
                       'total_bytes_used_for_headers_in_the_forward_direction\n')

    print("################### Writing the data #############################")
    pkts = []
    global processed_data
    id = 0
    for pkt in capture:
        try:
            id += 1
            protocol = pkt.transport_layer
            src_addr = pkt.ip.src
            src_port = pkt[pkt.transport_layer].srcport
            dst_addr = pkt.ip.dst
            dst_port = pkt[pkt.transport_layer].dstport

            flow = "protocol:" + str(protocol) + ", ip_src:" + \
                   str(src_addr) + ", src_port: " + str(src_port) + ", dst_addr:" + \
                   str(dst_addr) + ", dstport:" + str(dst_port)

            if flow not in processed_data:
                print("flow to analyze, " + flow)
                dataset.writelines(src_addr + ";" + dst_addr + ";" + src_port + ";" + dst_port + ";" +
                                   flow_features(protocol, capture, src_addr, src_port, dst_addr, dst_port) + "\n")

            # save the data whose are processing in a checklist
            processed_data.append(flow)
            processed_data.append("protocol:" + str(protocol) + ", ip_src:" + \
                                  str(dst_addr) + ", src_port: " + str(src_port) + ", dst_addr:" + \
                                  str(src_addr) + ", dstport:" + str(dst_port))
        except AttributeError:
            pass
        except Exception:
            print("Error during the pcap process")
    return pkts


def flow_features(protocol, capture, src_addr, src_port, dst_addr, dst_port):
    duration_flow_first = 0.0
    duration_flow = 0.0
    number_bytes_sent_per_flow = 0
    number_bytes_received_per_flow = 0
    total_bytes_headers_forward_direction = 0
    i = 0
    for pkt in capture:

        if pkt.transport_layer == protocol and pkt.ip.src == src_addr and pkt.ip.dst == dst_addr \
                and pkt[protocol].dstport == dst_port and pkt[protocol].srcport == src_port:
            try:
                number_bytes_sent_per_flow = number_bytes_sent_per_flow + int(pkt.captured_length)
            except Exception:
                number_bytes_sent_per_flow = 0
                print("Exception during the number of bytes sent per flow")
            try:
                if i == 0:
                    duration_flow_first = float(pkt.frame_info.time_epoch)
                i += 1
                duration_flow = float(pkt.frame_info.time_epoch) - duration_flow_first
            except Exception:
                print("Exception during the duration feature")
                duration_flow = 0
            try:
                if pkt.transport_layer == protocol and pkt.ip.src == dst_addr and pkt.ip.dst == src_addr \
                        and pkt[protocol].dstport == dst_port and pkt[protocol].srcport == src_port:
                    number_bytes_received_per_flow = number_bytes_received_per_flow + pkt.captured_length
            except Exception:
                print("Exception during the number bytes received per flow")
                number_bytes_received_per_flow = 0

            total_bytes_headers_forward_direction = float(pkt['IP'].hdr_len)
            if pkt.transport_layer == 'TCP':
                total_bytes_headers_forward_direction = total_bytes_headers_forward_direction + float(
                    pkt['TCP'].hdr_len)
    return str(duration_flow) + ";" + str(number_bytes_sent_per_flow) + ";" + \
           str(number_bytes_received_per_flow) + ";" + str(total_bytes_headers_forward_direction)


def main():
    """
    The main method allows us to define the activity to do in our program
    """
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
    pkt.show()  # debug statement


if __name__ == "__main__":
    main()
