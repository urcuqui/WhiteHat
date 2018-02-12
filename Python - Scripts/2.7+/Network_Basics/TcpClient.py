#Python 2.7
#Christian Urcuqui
import socket

target_host = "www.google.com"
target_port = 80
#target_host = "0.0.0.0"
#target_port = 9999

#https://docs.python.org/2/library/socket.html
#socket.AF_UNIX
#socket.AF_INET ... this is the stantard IPv4
#socket.AF_INET6
#These constants represent the address (and protocol) families, used for the first argument to socket(). If the AF_UNIX constant is not defined then this protocol is unsupported.
#and
#socket.SOCK_STREAM ... This is TCP
#socket.SOCK_DGRAM  ... This is UDP
#socket.SOCK_RAW
#socket.SOCK_RDM
#socket.SOCK_SEQPACKET
#These constants represent the socket types, used for the second argument to socket(). (Only SOCK_STREAM and SOCK_DGRAM appear to be generally useful.)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

#Message will send
client.send("GET / HTTP/1.1/r\nHost: google.com\r\n\r\n")

#socket.recv(bufsize[, flags])
response = client.recv(4096)

print response
