#Python 3
#Christian Urcuqui
import socket

target_host = "localhost"
target_port = 9999

# create a socket object
#https://docs.python.org/2/library/socket.html
#socket.AF_UNIX
#socket.AF_INET ... this is the stantard IPv4
#socket.AF_INET6
#These constants represent the address (and protocol) families, used for the first argument to socket().
# If the AF_UNIX constant is not defined then this protocol is unsupported.
#and
#socket.SOCK_STREAM ... This is TCP
#socket.SOCK_DGRAM  ... This is UDP
#socket.SOCK_RAW
#socket.SOCK_RDM
#socket.SOCK_SEQPACKET
#These constants represent the socket types, used for the second argument to socket(). (Only SOCK_STREAM and SOCK_DGRAM appear to be generally useful.)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send some data
client.sendto(b"AAABBBCCC", (target_host, target_port))
# receive some data
#socket.recv(bufsize[, flags])
data, addr = client.recvfrom(4096)
print(data)