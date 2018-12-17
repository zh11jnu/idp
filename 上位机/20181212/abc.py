import socket
import threading
import struct
import os
import time
import sys
import numpy
import cv2
import re
import queue
from multiprocessing import Process


#gmutex = threading.Lock()
class webCamConnect:

    def __init__(self, resolution=[640, 480], remoteAddress=("192.168.0.105",
                                                             8021), windowName="video"):
        self.remoteAddress = remoteAddress
        self.resolution = resolution
        self.name = windowName
        # self.mutex = threading.Lock()
        self.src = 911 + 15
        self.interval = 0
        self.path = os.getcwd()
        self.img_quality = 15
        # self.img_pipe = []
        self.img_pipe = queue.Queue()
        self.count=0
        self.image=0

    def read(self):
        #
        #time.sleep(1)
        #while(1):
        if(self.img_pipe.empty()):
            return 0,None
        img =self.img_pipe.get()
        return 1,img
        #return self.image
        # self.mutex.release()
        # 

    def _setSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        self._setSocket()
        print(self.remoteAddress)
        self.socket.connect(self.remoteAddress)

    def _processImage(self):
        self.socket.send(struct.pack(
            "lhh", self.src, self.resolution[0], self.resolution[1]))
        while(1):
            info = struct.unpack("lhh", self.socket.recv(8))
            bufSize = info[0]
            if bufSize:
                try:
                    #self.mutex.acquire()
                    self.buf = b''
                    tempBuf = self.buf
                    while(bufSize):  # 循环读取到一张图片的长度
                        tempBuf = self.socket.recv(bufSize)
                        bufSize -= len(tempBuf)
                        self.buf += tempBuf
                        data = numpy.fromstring(self.buf, dtype='uint8')
                        #self.img_pipe.put(data.copy())

                        


                        #gmutex.acquire()
                        self.image = cv2.imdecode(data, 1)
                        self.count+=1
                        print("thead:%d"%self.count)
                        cv2.imshow(self.name, self.image.copy())
                        self.img_pipe.put(self.image.copy())
                        # abc = self.img_pipe.get()
                        #gmutex.release() 


                        # cv2.imshow("self.nam", abc)

                        # if (abc==self.image.copy()).all():
                        #     print("ok")
                except Exception as e:
                    print(e)
                    print("接收失败")
                    pass
                finally:
                    #self.mutex.release()
                    if cv2.waitKey(10) == 27:
                        self.socket.close()
                        cv2.destroyAllWindows()
                        print("放弃连接")
                        break

    def getData(self, interval):
        #showThread = threading.Thread(target=self._processImage)
        showThread = Process(target=self._processImage)
        # Process
        showThread.start()
        #showThread.join()

    def setWindowName(self, name):
        self.name = name

    def setRemoteAddress(remoteAddress):
        self.remoteAddress = remoteAddress


    def check_config(self):
        path = os.getcwd()
        print(path)
        if os.path.isfile(r'%s\video_config.txt' % path) is False:
            f = open("video_config.txt", 'w+')
            print("w = %d,h = %d" % (self.resolution[0], self.resolution[1]), file=f)
            print("IP is %s:%d" % (self.remoteAddress[0], self.remoteAddress[1]), file=f)
            print("Save pic flag:%d" % (self.interval), file=f)
            print("image's quality is:%d,range(0~95)" % (self.img_quality), file=f)
            f.close()
            print("初始化配置")
        else:
            f = open("video_config.txt", 'r+')
            tmp_data = f.readline(50)  # 1 resolution
            num_list = re.findall(r"\d+", tmp_data)
            self.resolution[0] = int(num_list[0])
            self.resolution[1] = int(num_list[1])
            tmp_data = f.readline(50)  # 2 ip,port
            num_list = re.findall(r"\d+", tmp_data)
            str_tmp = "%d.%d.%d.%d"%(int(num_list[0]), int(num_list[1]), int(num_list[2]), int(num_list[3]))
            self.remoteAddress = (str_tmp, int(num_list[4]))
            tmp_data = f.readline(50)  # 3 savedata_flag
            self.interval = int(re.findall(r"\d", tmp_data)[0])
            tmp_data = f.readline(50)  # 3 savedata_flag
            # print(tmp_data)
            self.img_quality = int(re.findall(r"\d+", tmp_data)[0])
            # print(self.img_quality)
            self.src = 911 + self.img_quality
            f.close()
            print("读取配置")


def main():
    print("创建连接...")
    cam = webCamConnect()
    cam.check_config()
    print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
    print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
    print("目标ip为%s:%d" % (cam.remoteAddress[0], cam.remoteAddress[1]))
    cam.connect()
    cam.getData(cam.interval)
    i=100

    while(True):
        i -= 1
        print("main wait Lock")
        #gmutex.acquire()
        ret,img = cam.read()
        if (ret==1):
            cv2.imshow("1",img)
            print("main:%d"%cam.count)
        #gmutex.release()
        cv2.waitKey(10)



if __name__ == "__main__":
    main()
