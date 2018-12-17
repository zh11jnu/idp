import camera_client


print("创建连接...")
cam = camera_client.webCamConnect()
cam.check_config()
print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
print("像素为:%d * %d" % (cam.resolution[0], cam.resolution[1]))
print("目标ip为%s:%d" % (cam.remoteAddress[0], cam.remoteAddress[1]))
cam.connect()
cam.getData(cam.interval)
