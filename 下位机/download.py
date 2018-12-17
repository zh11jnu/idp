import socket
import struct
import os
import netifaces as ni
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a',
                    filename='/home/pi/logs/download.log')


def download_run_code(port=6788):
    host = ni.ifaddresses('wlan0')[2][0]['addr']
    port = 6788
    fmt = '128si'
    recv_buffer = 4096
    listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listenSock.bind((host, port))
    while True:
        listenSock.listen(5)
        conn, addr = listenSock.accept()
        headsize = struct.calcsize(fmt)
        head = conn.recv(headsize)
        filename = struct.unpack(fmt, head)[0].decode().rstrip('\0')
        filename = '/home/pi/' + filename
        filesize = struct.unpack(fmt, head)[1]
        logging.info("filename:" + filename + "   filesize:" + str(filesize))
        recved_size = 0
        fd = open(filename, 'wb')
        # count = 0
        while True:
            data = conn.recv(recv_buffer)
            recved_size = recved_size + len(data)
            fd.write(data)
            if recved_size == filesize:
                break
        fd.close()
        logging.info("new file")
        logging.info(os.popen("python test.py").read())
