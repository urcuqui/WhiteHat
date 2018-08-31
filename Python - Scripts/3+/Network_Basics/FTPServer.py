import socket

socket.setdefaulttimeout(2)
s = socket.socket()
print(socket.gethostbyname("ftp://speedtest.tele2.net"))

#s.connect(("speedtest.tele2.net/", 21))
ans = s.recv(1024)
print(ans)
