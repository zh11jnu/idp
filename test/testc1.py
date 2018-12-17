import socket

from datetime import datetime

address = ('192.168.0.106',6789)

max_size =1000


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(address)

client.sendall(b'Hey~~~')

data = client.recv(max_size)

print("some reply" , data)

client.close()
