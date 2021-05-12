# pylint: disable = no-member

import os
import random
from matplotlib import pyplot
from math import sqrt, ceil
from numpy import expand_dims
from keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
import cv2
from Function import CreateDataset, DatasetSample, MakeDir


def DataAugmentationKeras(dataset, number_of_aug_data, save_data_folder=None, save_prefix='', plot=False):
    # Flip, Rotation, Shift, Brightness, Zoom
    # dataset is a list
    for test_element in dataset:
        img = load_img(test_element)
        array = img_to_array(img)
        samples = expand_dims(array, 0)
        datagen = ImageDataGenerator(
            horizontal_flip=True,
            vertical_flip=True,
            rotation_range=90,
            width_shift_range=80,
            height_shift_range=80,
            brightness_range=[0.2, 1.8],
            zoom_range=[0.5, 1.5]
        )
        i = 0
        # generate samples and plots
        for batch in datagen.flow(samples, batch_size=1,
                                  save_to_dir=save_data_folder,
                                  save_prefix=save_prefix, save_format='jpeg'):
            if plot == True:
                axis = ceil(sqrt(number_of_aug_data))
                if i == 0:
                    # define subplot
                    pyplot.subplot(axis, axis, 1)
                    pyplot.imshow(img)
                pyplot.subplot(axis, axis, 2 + i)
                # convert to unsigned integers for viewing
                # batch have shape (1, width, height, channel). Index [0] to get (width, height, channel)
                image = batch[0].astype('uint8')
                # plot raw pixel data
                pyplot.imshow(image)
            i += 1
            if i >= number_of_aug_data:
                break
    if plot == True:
        # show the figure
        pyplot.show()


data_dirs = 'data\\'
subsets = ['000_hatsune_miku\\', '018_kagamine_rin\\', '021_hirasawa_yui\\']

data = CreateDataset(data_dirs, subsets)
test_data = DatasetSample(data, mode='specific')
aug_data_folder = MakeDir('aug_data_keras')
DataAugmentationKeras(test_data, number_of_aug_data=8,
                      save_data_folder=None, save_prefix='aug_data', plot=True)
