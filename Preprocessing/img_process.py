import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
import math
import shutil
import tensorflow as tf
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
from PIL import Image
from six.moves import range

data_folder  = './Image/image'
train_folder = './Image/train'
test_folder = './Image/test'
dimensions  = (224, 224)
max_angle = 15

def process_images(folder):

    classes = [os.path.join(folder, d) for d in sorted(os.listdir(folder))]  # get list of all sub-folders in folder
    img_cnt = 0

    for class_x in classes:

        if os.path.isdir(class_x):

            # get paths to all the images in this folder
            images = [os.path.join(class_x, i) for i in sorted(os.listdir(class_x)) if i != '.DS_Store']


            for image in images:

                img_cnt = img_cnt + 1

                if(img_cnt % 1000 == 0):
                    print("Processed %s images" % str(img_cnt))

                im = Image.open(image)
                im = im.resize(dimensions)   # resize image according to dimensions set
                im.save(image)   # overwrite previous image file with new image

    print("Finished processing images, images found = ")
    print(img_cnt)


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


def split_images(folder):

    classes = [os.path.join(folder, d) for d in sorted(os.listdir(folder))]  # get list of all sub-folders in folder
    total_img_count , img_cnt, total_image, train_size, test_size = 0, 0, 0,0, 0

    for i, class_x in enumerate(classes):

        if os.path.isdir(class_x):

            # get paths to all the images in this folder
            images = [os.path.join(class_x, i) for i in sorted(os.listdir(class_x)) if i != '.DS_Store']

            total_image = [image for image in images]
            total_image = len(total_image)
            train_size = math.ceil(total_image*.8)
            test_size = math.floor(total_image*.2)
            createFolder('./Image/train/'+str(i+1))
            createFolder('./Image/test/'+str(i+1))
            train_path = './Image/train/'+str(i+1)
            test_path = './Image/test/'+str(i+1)

            for image in images:

                img_cnt = img_cnt + 1
                total_img_count = total_img_count + 1

                if img_cnt <= train_size:
                    shutil.copy(image, train_path)
                else:
                    shutil.copy(image, test_path)


            img_cnt, total_image, train_size, test_size = 0, 0, 0,0
            print(train_path)
        print(class_x, i+1)
    print("Finished processing images, images found = ")
    print(total_img_count)

process_images(data_folder)
split_images(data_folder)
