#!/usr/bin/env python3
from PIL import Image
import numpy as np
import os
import cv2

path = r'C:\Users\Sphinx\Desktop\numpy\Data\val'
files = os.listdir(path)


def grabArrayOfImages(files,resizeW=64,resizeH=64,gray=False):

    total_folder = 0
    imageArr = []
    for file_index, file in enumerate(files):
        file_path = os.path.join(path, file)
        print(file_path)
        total_folder = total_folder + 1

        if gray:
                im = Image.open(file_path).convert("L")
        else:
            im = Image.open(file_path).convert("RGB")

        im = im.resize((resizeW,resizeH))
        imData = np.asarray(im)
        imageArr.append(imData)

    return imageArr


    print("After preprocessing(rename): image number: ", total_folder)



imageArrGray = grabArrayOfImages(files,resizeW=64,resizeH=64,gray=True)
imageArrColor = grabArrayOfImages(files,resizeW=64,resizeH=64)

print("Shape of ImageArr Gray: ", np.shape(imageArrGray))
print("Shape of ImageArr Color: ", np.shape(imageArrColor))
cv2.imread(imageArrColor[0])
np.save('./Data/church_outdoor_train_lmdb_gray.npy', imageArrGray)
np.save('./Data/church_outdoor_train_lmdb_color.npy', imageArrColor)

# listOfFiles = grabListOfFiles(direc)
# imageArrGray = grabArrayOfImages(listOfFiles,resizeW=64,resizeH=64,gray=True)
# imageArrColor = grabArrayOfImages(listOfFiles,resizeW=64,resizeH=64)
# print("Shape of ImageArr Gray: ", np.shape(imageArrGray))
# print("Shape of ImageArr Color: ", np.shape(imageArrColor))
# np.save('/data/church_outdoor_train_lmdb_gray.npy', imageArrGray)
# np.save('/data/church_outdoor_train_lmdb_color.npy', imageArrColor)
