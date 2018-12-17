import socket
import picamera
import time
import struct
import numpy as np
import io

host = ('192.168.0.105', 8887)
resolution = (3280, 2464)
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind(host)
soc.listen(5)
client, addr = soc.accept()
command = str(client.recv(32), encoding="utf-8")
print(command)
if command == "picture":
    with picamera.PiCamera() as camera:
        camera.resolution = (resolution[0], resolution[1])
        time.sleep(1)

        # data = np.empty((resolution[0] * resolution[1] * 3,), dtype=np.uint8)
        stream = io.BytesIO()
        camera.capture(stream, format='jpeg')
        image = stream.getvalue()
        print(type(image))
        print(len(image))
        client.send(struct.pack("lhh", len(image), resolution[
                    0], resolution[1]) + image)
        stream.truncate()
        stream.seek(0)
soc.close()
