import sys
import socket
import threading
def server_loop(local_host,local_port,remote_host,remote_port,receive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host,local_port))
    except:
        print "[!!] Failed to listen on %s:%d" %(local_host,local_port)
        print "[!!] Check for other listening sockets or correct permissions."
        sys.exit()

    print "[*] Listening on %s:%d" %(local_host,local_port)
    server.listen(5)
    while True:
        client_socket, addr = server.accept()

        # Print out the local connection information
        print "[==>] Received incoming coneciton from %s:%d" %(addr[0],addr[1])

        # Start a thread to talk to the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

    def main():

        # No fancy command-line parsing here
        if len(sys.argv[1:]) != 5:
            print "Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_port]"
            print "Example: ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True"
            sys.exit()

        # setup local listening parameters
        local_host = sys.argv[1]
        local_port = int(sys.argv[2])

        # setup remote target
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])