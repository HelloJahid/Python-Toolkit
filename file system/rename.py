import os
path = '/home/alpha/Desktop/Rename/1'
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, 'one.'+str(index)+'.png'))
