import socket 
localIP = socket.gethostbyname(socket.gethostname())
print("local ip:%s "%localIP)