import socket

target_host = "localhost"
target_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((target_host, target_port))

#Message will send
client.send("GET / HTTP/1.1/r\nHost: google.com\r\n\r\n")

response = client.recv(4096)

print(response)
