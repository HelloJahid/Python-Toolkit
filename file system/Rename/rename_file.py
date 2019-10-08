import os
path = r'C:\Users\Sphinx\Desktop\Python-Toolkit\Sign Data\0'
files = os.listdir(path)


for index, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, '0zero.'+str(index)+'.png'))
