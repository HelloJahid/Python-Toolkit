import os
import cv2
from PIL import Image
from resizeimage import resizeimage


path = r'C:\Users\Sphinx\Desktop\Python-Toolkit\maiz_train\8'

files = os.listdir(path)

print(files)

for index, file in enumerate(files):

    # fd_img = open(os.path.join(path, file), 'r')
    img = Image.open(os.path.join(path, file))
    img = resizeimage.resize_contain(img, [299, 299])
    img.save(os.path.join(path, file), img.format)
    print("preprocessing(resize): image number: ", index+1)
