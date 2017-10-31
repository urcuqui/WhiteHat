#Python 2.7
#Christian Urcuqui
#This class has a some functions of Netcat, a utility knife of networking

import sys
import socket
import getopt  # getopt — C-style parser for command line options
import threading
import subprocess
# https://docs.python.org/2/library/sys.html
# https://docs.python.org/2/library/getopt.html
# https://docs.python.org/2/library/subprocess.html
# These are some global variables
listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


# Useful usage information
def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen"
    print "-e --execute=file_to_run"
    print "-c --command"
    print "-u --upload=destination"
    print
    print
    print "Examples:"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)


# main function is responsible for handling command line arguments and calling the rest of our functions
def main():
    # The next lines declare the global variables
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    # sys.argv[]
    # The list of command line arguments passed to a Python script. argv[0] is the script name (it is operating system
    # dependent whether this is a full pathname or not). If the command was executed using the -c command line option to
    # the interpreter, argv[0] is set to the string '-c'. If no script name was passed to the Python interpreter, argv[0]
    # is the empty string.
    if not len(sys.argv[1:]):
        usage()

    #it reads the commandline options
    try:
        #getopt.getopt(args, options[, long_options])
        #Parses command line options and parameter list. args is the argument list to be parsed, without the leading reference
        #to the running program. Typically, this means sys.argv[1:]. options is the string of option letters that the script wants
        # to recognize, with options that require an argument followed by a colon (':'; i.e., the same format that Unix getopt() uses).
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu", [["help", "listen", "execute", "target", "port",
                                                                "command", "upload"]])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
        if o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)

        else:
            assert False, "Unhandled Option"

    # are we going to listen or just send data from stdin?
    if not listen and len(target) and port > 0:
        # The buffer is reading from the command line
        # so, if we would like to stop it, we need to send CTRL-D
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)
    # we are going to listen and potentially
    # upload things, execute commands, and drop shell back
    # depending on our command line options above
    if listen:
        server_loop()


def client_sender(buffer):
    # TCP
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((target, port))
        if len(buffer):
            client.send(buffer)

        while True:
            # Now it will wait for data back
            recv_len = 1
            response = ""
            # we will receive back data until there is no more data to receive
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += (data).decode('utf-8')
                if recv_len < 4096:
                    break
            print response,

            # wait for more input
            buffer = input("")
            buffer += "\n"
            client.send((buffer).encode('utf-8'))

    except:

        print("[*] Exception! Existing.")
        client.close()


def server_loop():
    global target
    if not len(target):
        target = "0.0.0.0"
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target, port))
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        # spin off a thread to handle our new client
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()


def run_command(command):

    # trim the newline
    command = command.rstrip()

    # run the command and get the output back
    try:
        #subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, universal_newlines=False)
        #Run command with arguments and return its output as a byte string.
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "failed to execute command. \r\n"
    # send the output back to the client
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for our upload destination
    if len(upload_destination):
        # read in all of the bytes and write to our destination
        file_buffer = ""
        # keep reading data until none is available
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            else:
                file_buffer += data
        # now we take these bytes and try to write them out
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            # acknowledge that we wrote the file out
            client_socket.send("Successfully saved to file %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)
    # check for command execution
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)
    # now we go into another loop if a command shell was requested
    if command:
        while True:
            # show a simple prompt
            #client_socket.send(("<BHP:#>").encode('utf-8'))
            client_socket.send("<BHP:#>")
            # now we receive until we see a linefeed (enter key)
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                #cmd_buffer += (client_socket.recv(1024)).decode('utf-8')
                cmd_buffer += client_socket.recv(1024)

            # send back the command output
            response = run_command(cmd_buffer)

            # send back the response
            client_socket.send(response)

main()
