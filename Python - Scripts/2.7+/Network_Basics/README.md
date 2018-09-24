# Network Basic

General concepts:
+ Socket, is a media that allows two things to communicate, it is a mechanism to get and sent flow of information that its composed by packets, such as UDP and TCP/IP.
+ UDP is a protocol that is not oriented to a connection, nevertheless, TCP is is oriented to a connection so some of the packages might not loss in the communication
+ ACK, a flag used in the Transmission Control Protocol (TCP) to acknowledge receipt of a packet
+ Packet analyzer, it is a program or hardware to capture log traffic over digital network or part of a network.
+ Proxy server, it is a server and it is be an intermediary for requests between clients and other servers. It is useful
 to control the requests and the access to content on the World Wide Web.
+ Netcat, it is a networking utility to write and read from network connections using TCP or UDP.
+ SSH (Secure Shell), it is a media to connect a server by secure shell, in conclusion it is used to be a user interface
 for access to an operating system resources. 

These are the python files in this directory:
+ TCP Client, it is a code to create a web client with TCP socket. 
+ UDP Client, it is a code to create a web client with UDP socket. 
+ TCP Server, it is a code to create a web server with TCP socket.  
+ UDP Server, it is a code to create a web server with TCP socket. 
+ Proxy, it is a code to create a proxy server in python in order to capture some packets.
+ bhpnet, it is a Netcat tool in Python. In the same file it has both client and server environment in TCP.


## Examples with the scripts

## Netcat with Python

We can use the script bhpnet in order to execute commands like the netcat tool, for example use the
next command with the python file

```
echo -ne "GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n" | bhpnet.py -t www.google.com -p 80
```
