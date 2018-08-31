#Python 2.7
#Christian Urcuqui
import socket

# --- Example of a server that is listening with a UDP protocol ---
# https://docs.python.org/2/library/socket.html#socket.socket.recv
# https://docs.python.org/2/library/threading.html
bind_ip = '0.0.0.0'
bind_port = 9999
#socket.AF_INET ... this is the stantard IPv4
#socket.SOCK_DGRAM  ... This is UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server.bind((bind_ip, bind_port))

print("[*] Listening on %s:%d" % (bind_ip, bind_port))

while True:

    print 'waiting to receive message'
    data, addr = server.recvfrom(4026)
    print 'received %s bytes from %s' % (len(data), addr)
    print data
    if data:
        server.sendto('que ondas!', addr)