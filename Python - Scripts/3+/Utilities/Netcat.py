#Python 3
#Christian Urcuqui

#libraries
import sys
import socket
import getopt # this is a package to get commands in python
import threading
import subprocess # # this is an module that allows us to spawn new processes, connect to their input/error pipes

# We are going to define some global variables

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


# The next method allows us to define the commands options for our netcat tool
def usage():
    print("BHP Net tool")
    print()
    print("Usage bhpnet.py -t target_host -p port")
    print("-l --listen                  - listen on [host]:[port] for incoming connections")
    print("-e --execute=file_to_run     - execute the given file upon receiving a connection")
    print("-c --command                 - initialize a command shell")
    print("-u --upload-destination      - upon receiving connection upload a file and write to [destination]")
    print("")
    print("")
    print("Examples: ")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -c")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe")
    print("bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\"")
    sys.exit(0)


def main():
    global listen
    global port
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen", "execute", "target",
                                                                 "port", "command","upload"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command =  True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unhanlded Option"

        # are we going to listen or just send data from stdin?
        if not listen and len(target) and port >0:
            # read in the buffer from the commandLIne
            # this will block, so send CTRL-D if not sending input to stdin
            buffer = sys.stdin.read()


"""
References
+ https://docs.python.org/3.7/library/getopt.html
+ https://docs.python.org/3.7/library/subprocess.html
+ Black Hat Python -  Justin Seitz

"""

