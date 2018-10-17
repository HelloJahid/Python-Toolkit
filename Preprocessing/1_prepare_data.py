
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
import tensorflow as tf
from IPython.display import display, Image
from scipy import ndimage
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle
from PIL import Image
from six.moves import range

train_folder  = './data/train'
test_folder  = './data/valid'
dimensions  = (229, 229)
max_angle = 15


# rotating image
def rotate_img(image, angle, color, filter = Image.NEAREST):

    if image.mode == "P" or filter == Image.NEAREST:
        matte = Image.new("1", image.size, 1) # mask
    else:
        matte = Image.new("L", image.size, 255) # true matte
    bg = Image.new(image.mode, image.size, color)
    bg.paste(
        image.rotate(angle, filter),
        matte.rotate(angle, filter)
    )
    return bg

# make gray_scale image or 1channel image
def make_greyscale_white_bg(im, r, b, g):

    im = im.convert('RGBA')   # Convert to RGBA


    data = np.array(im)   # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T # Temporarily unpack the bands for readability

    # Replace grey with white... (leaves alpha values alone...)
    grey_areas = (red == r) & (blue == b) & (green == g)
    data[..., :-1][grey_areas.T] = (255, 255, 255) # Transpose back needed

    im2 = Image.fromarray(data)
    im2 = im2.convert('L')   # convert to greyscale image



    #im2.show()

    return im2

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


process_images(test_folder)
process_images(train_folder)

print('ok')

image_size = 229  # Pixel width and height.
pixel_depth = 255.0  # Number of levels per pixel.


def load_letter(folder, min_num_images):


  image_files = os.listdir(folder)
  dataset = np.ndarray(shape=(len(image_files), image_size, image_size, 3), dtype=np.float32)
  print(dataset.shape)

  num_images = 0
  for image_index, image in enumerate(image_files):
    image_file = os.path.join(folder, image)
    try:
      image_data = (ndimage.imread(image_file).astype(float) - pixel_depth / 2) / pixel_depth
      print(image_data.shape)

      if image_data.shape != (image_size, image_size, 3):
        raise Exception('Unexpected image shape: %s' % str(image_data.shape))
      dataset[num_images, :, :] = image_data
      num_images = num_images + 1
    except IOError as e:
      print('Could not read:', image_file, ':', e, '- it\'s ok, skipping.')

  dataset = dataset[0:num_images, :, :]
  if num_images < min_num_images:
    raise Exception('Many fewer images than expected: %d < %d' %
                    (num_images, min_num_images))

  print('Full dataset tensor:', dataset.shape)
  print('Mean:', np.mean(dataset))
  print('Standard deviation:', np.std(dataset))
  return dataset

def maybe_pickle(data_folders, min_num_images_per_class, force=False):
  dataset_names = []
  folders_list = os.listdir(data_folders)
  for folder in folders_list:


    #print(os.path.join(data_folders, folder))
    curr_folder_path = os.path.join(data_folders, folder)
    if os.path.isdir(curr_folder_path):
        set_filename = curr_folder_path + '.pickle'
        dataset_names.append(set_filename)
        if os.path.exists(set_filename) and not force:
  #         # You may override by setting force=True.
          print('%s already present - Skipping pickling.' % set_filename)
        else:
          print('Pickling %s.' % set_filename)
          dataset = load_letter(curr_folder_path, min_num_images_per_class)
          try:
            with open(set_filename, 'wb') as f:
                pickle.dump(dataset, f, pickle.HIGHEST_PROTOCOL)
                f.close()
          except Exception as e:
            print('Unable to save data to', set_filename, ':', e)

  return dataset_names

train_datasets = maybe_pickle(train_folder, 89, True)
test_datasets = maybe_pickle(test_folder, 10, True)


def make_arrays(nb_rows, img_size):
  if nb_rows:
    dataset = np.ndarray((nb_rows, img_size, img_size, 3), dtype=np.float32)
    labels = np.ndarray(nb_rows, dtype=np.int32)
  else:
    dataset, labels = None, None
  return dataset, labels

def merge_datasets(pickle_files, train_size, valid_size=0):
  num_classes = len(pickle_files)
  valid_dataset, valid_labels = make_arrays(valid_size, image_size)
  train_dataset, train_labels = make_arrays(train_size, image_size)
  vsize_per_class = valid_size // num_classes
  tsize_per_class = train_size // num_classes

  start_v, start_t = 0, 0
  end_v, end_t = vsize_per_class, tsize_per_class
  end_l = vsize_per_class+tsize_per_class
  for label, pickle_file in enumerate(pickle_files):
    try:
      with open(pickle_file, 'rb') as f:
        letter_set = pickle.load(f)
        f.close()
        # let's shuffle the letters to have random validation and training set
        np.random.shuffle(letter_set)
        if valid_dataset is not None:
          valid_letter = letter_set[:vsize_per_class, :, :]
          valid_dataset[start_v:end_v, :, :] = valid_letter
          valid_labels[start_v:end_v] = label
          start_v += vsize_per_class
          end_v += vsize_per_class

        train_letter = letter_set[vsize_per_class:end_l, :, :]
        train_dataset[start_t:end_t, :, :] = train_letter
        train_labels[start_t:end_t] = label
        start_t += tsize_per_class
        end_t += tsize_per_class
    except Exception as e:
      print('Unable to process data from', pickle_file, ':', e)
      raise

  return valid_dataset, valid_labels, train_dataset, train_labels


train_size = 89
valid_size = 10


valid_dataset, valid_labels, train_dataset, train_labels = merge_datasets(
  train_datasets, train_size, valid_size)
# _, _, test_dataset, test_labels = merge_datasets(test_datasets, test_size)

print('Training:', train_dataset.shape, train_labels.shape)
print('Validation:', valid_dataset.shape, valid_labels.shape)
# print('Testing:', test_dataset.shape, test_labels.shape)

def randomize(dataset, labels):
  permutation = np.random.permutation(labels.shape[0])
  shuffled_dataset = dataset[permutation,:,:]
  shuffled_labels = labels[permutation]
  return shuffled_dataset, shuffled_labels
train_dataset, train_labels = randomize(train_dataset, train_labels)
# test_dataset, test_labels = randomize(test_dataset, test_labels)
valid_dataset, valid_labels = randomize(valid_dataset, valid_labels)


pickle_file = './bacteria.pickle'

try:
  f = open(pickle_file, 'wb')
  save = {
    'train_dataset': train_dataset,
    'train_labels': train_labels,
    'valid_dataset': valid_dataset,
    'valid_labels': valid_labels,
    }
  pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
  f.close()
except Exception as e:
  print('Unable to save data to', pickle_file, ':', e)
  raise


statinfo = os.stat(pickle_file)
print('Compressed pickle size:', statinfo.st_size)
