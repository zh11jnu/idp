import socket
import struct
import numpy
import cv2

remoteAddress = ('192.168.0.105', 8887)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.connect(remoteAddress)
soc.send(bytes('picture', encoding="utf8"))

info = struct.unpack("lhh", soc.recv(8))
bufSize = info[0]
if bufSize:
    buf = b''
    tempBuf = buf
    while(bufSize):  # 循环读取到一张图片的长度
        tempBuf = soc.recv(bufSize)
        bufSize -= len(tempBuf)
        buf += tempBuf
    data = numpy.fromstring(buf, dtype='uint8')
    image = cv2.imdecode(data, 1)
    #cv2.imshow("1", image)
    cv2.imwrite("1.jpeg", image)
soc.close()
