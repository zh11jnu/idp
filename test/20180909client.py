import socket
import os
import struct
import tkinter
import camera_client


def Button1():
    downpath = r'F:/test45.py'
    fp = open(downpath, "w")
    fp.write('print("abc123123")')
    fp.write('ifconfig')
    fp.close()
    host = ('192.168.0.104', 6788)
    fmt = '128si'
    send_buffer = 4096
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(host)
    filepath = downpath
    filename = os.path.split(filepath)[1]
    filesize = os.path.getsize(filepath)
    print("filename:" + filename + "  filesize:" + str(filesize))
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


def Button2():
    print("创建连接...")
    cam = camera_client.webCamConnect()
    cam.check_config()
    print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
    print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
    print("目标ip为%s:%d" % (cam.remoteAddress[0], cam.remoteAddress[1]))
    cam.connect()
    cam.getData(cam.interval)


root = tkinter.Tk()
btn1 = tkinter.Button(root, text='Button1',
                      command=Button1).grid(row=1, column=1, sticky='E')
btn2 = tkinter.Button(root, text='Button2',
                      command=Button2).grid(row=2, column=1, sticky='E')
root.mainloop()
