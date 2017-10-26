import socket

# --- Example of a server that is listening with a UDP protocol ---

bind_ip = '0.0.0.0'
bind_port = 9999

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