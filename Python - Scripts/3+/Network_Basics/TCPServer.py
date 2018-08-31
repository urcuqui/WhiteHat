#Python 3
#Christian Urcuqui
import socket
import threading
import datetime
# --- Example of a server that is listening with a TCP protocol ---
# https://docs.python.org/2/library/socket.html#socket.socket.recv
# https://docs.python.org/2/library/threading.html
bind_ip = '0.0.0.0'
bind_port = 8013


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#socket.bind(address)
#Bind the socket to address. The socket must not already be bound.
server.bind((bind_ip,bind_port))
#socket.listen(backlog)
#Listen for connections made to the socket. The backlog argument specifies the maximum number of queued connections and should be at least 0; the maximum value is system-dependent (usually 5), the minimum value is forced to 0.
server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip, bind_port))


def handle_client(client_socket):
    request = client_socket.recv(4026)

    print("[*] Received: %s" % request)
    client_socket.send(b'Hi from the server')

    client_socket.close()

#This is a loop, it is useful in order that the web server will listen client requests
while True:

    client, addr = server.accept()
    print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))
    # spin up our client thread to handle incoming data
    # target is the callable object to be invoked by the run() method. Defaults to None, meaning nothing is called.
    # args is the argument tuple for the target invocation. Defaults to ().
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
