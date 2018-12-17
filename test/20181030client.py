import socket
import os
import struct
import tkinter



def Module_grey():
    a = "import abc"


def Module_thresh():
    a += "\n import time"


def sendfiel():
    wtite(a)
    fp = open("F:/test.py", "w")
    fp.write('print("abc")')
    fp.write('ifconfig')
    fp.close()
    host = ('192.168.0.105', 6788)
    fmt = '128si'
    send_buffer = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(host)
    filepath = "F:/test.py"
    filename = os.path.split(filepath)[1]
    filesize = os.path.getsize(filepath)
    print("filename:" + filename + "\nfilesize:" + str(filesize))
    head = struct.pack(fmt, filename.encode(), filesize)
    print("\nhead size:" + str(head.__len__()) + "\n" + str(head))
    sock.sendall(head)
    restSize = filesize
    fd = open(filepath, 'rb')
    count = 0
    while restSize >= send_buffer:
        data = fd.read(send_buffer)
        sock.sendall(data)
        restSize = restSize - send_buffer
        print(str(count) + " ")
        count = count + 1
    data = fd.read(restSize)
    sock.sendall(data)
    fd.close()


root = tkinter.Tk()
Button1 = tkinter.Button(root, text='Button1',
                         command=Button1).pack(side=tkinter.LEFT)
root.mainloop()
