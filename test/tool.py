import os
from shutil import copyfile


def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return(files)
files = file_name("F:/test/all")
os.mkdir("F:/test/body")
os.mkdir("F:/test/car")
os.mkdir("F:/test/face")
for file in files:
    if "body" in file:
        f_body1 = "F:/test/all/"+file
        f_body2 = "F:/test/body/"+file
        copyfile(f_body1,f_body2 )
    if "car" in file:
        f_car1 = "F:/test/all/"+file
        f_car2 = "F:/test/car/"+file
        copyfile(f_car1,f_car2 )
    if "face" in file:
        f_face1 = "F:/test/all/"+file
        f_face2 = "F:/test/face/"+file
        copyfile(f_face1,f_face2 )