import shutil, os

source_path = '/home/alpha/Desktop/move file/images/'
dest_path = '/home/alpha/Desktop/move file/test/'

files = ['file11.txt']
for f in files:
    shutil.move(source_path+f, dest_path)
