import os
from shutil import copyfile
def file_name(file_dir):
    for root, dirs, files in os.walk(file_dir):
        return(files)
mainpath = 'F:/test/'
files = file_name(mainpath + 'all')
findlist = ['body', 'car', 'face']
list(map(lambda dirname: os.mkdir('F:/test/' + dirname), findlist))
for file in files:
    list(map(lambda find: copyfile(mainpath + 'all/' + file, mainpath + find + '/' + file) if find in file else 0, findlist))
