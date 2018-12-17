import socket, os, struct
 
host = ('192.168.0.106',6788)
fmt = '128si'
send_buffer = 4096
 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(host)
filepath = "F:/h.py"
filename = os.path.split(filepath)[1]
filesize = os.path.getsize(filepath)
print("filename:" + filename + "\nfilesize:" + str(filesize))
head = struct.pack(fmt, filename.encode(), filesize)
print("\nhead size:" + str(head.__len__()) + "\n" + str(head))
sock.sendall(head)
restSize = filesize
fd = open(filepath,'rb')
count = 0
while restSize >= send_buffer:
    data = fd.read(send_buffer)
    sock.sendall(data)
    restSize = restSize - send_buffer
    print(str(count)+" ")
    count = count + 1
data = fd.read(restSize)
sock.sendall(data)
fd.close()
print("successfully sent")