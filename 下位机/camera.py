import socket
import threading
import struct
import cv2
import time
import os
import numpy
import netifaces as ni
import logging
import io
import picamera


logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a',
                    filename='/home/pi/logs/camera.log')


class webCamera:

    def __init__(self, resolution=(640, 480), port=8021):
        self.resolution = resolution

        self.host = (ni.ifaddresses('wlan0')[2][0]['addr'], port)
        self.setSocket(self.host)
        self.img_quality = 15

    def setImageResolution(self, resolution):
        self.resolution = resolution

    def setHost(self, host):
        self.host = host

    def setSocket(self, host):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.host)
        self.socket.listen(5)
        logging.info("Server running on port:%d" % host[1])

    def recv_config(self, client):
        info = struct.unpack("lhh", client.recv(8))
        if info[0] > 911:  # print(info[0])
            self.img_quality = int(info[0]) - 911
            self.resolution = list(self.resolution)
            self.resolution[0] = info[1]
            self.resolution[1] = info[2]
            self.resolution = tuple(self.resolution)
            return 1
        else:
            return 0

    def _processConnection(self, client, addr):
        if(self.recv_config(client) == 0):
            return
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            time.sleep(1)
            #print('11')
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
                #print('a')
                #data = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
                #self.img_code = cv2.imdecode(data, 1)
                #print(type(stream.getvalue()))
                #self.imgdata = self.img_code.tostring()
                # cv2.imshow("img", image)
                # cv2.waitKey(1)
                self.image = stream.getvalue()
                print(len(self.image))
                # Truncate the stream to the current position (in case
                # prior iterations output a longer image)
                #stream.truncate()
                #stream.seek(0)
        # camera = cv2.VideoCapture(0)
        # encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.img_quality]
        # while(1):
        #     time.sleep(0.13)
        #     (grabbed, self.img) = camera.read()
        #     self.img = cv2.resize(self.img, self.resolution)
        #     result, imgencode = cv2.imencode('.jpg', self.img, encode_param)
        #     img_code = numpy.array(imgencode)
        #     self.imgdata = img_code.tostring()
                #try:
                client.send(struct.pack("lhh", len(self.image),
                                        self.resolution[0], self.resolution[1]) + self.image)
                #except Exception as e:
                #    print(e)
                stream.truncate()
                stream.seek(0)
                # camera.release()
                # f.close()
                #    return
                

    def run(self):
        while(1):
            client, addr = self.socket.accept()
            print('12')
            logging.info("on port:%d" % addr[1])
            clientThread = threading.Thread(target=self._processConnection,
                                            args=(client, addr, ))
            clientThread.start()


def main():
    cam = webCamera()
    cam.run()


if __name__ == "__main__":
    main()
