import threading
import time
import socket
from netaddr import IPNetwork,IPAddress

# host to listen on
host = "192.168.0.187"
# subnet to target
subnet = "192.168.0.0/24"
# magic string we'll check ICMP responses for
magic_message = "PYTHONRULES!"
# this sprays out the UDP datagrams


def udp_sender(subnet,magic_message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):
        try:
            sender.sendto(magic_message,("%s" % ip,65212))
        except:
            pass