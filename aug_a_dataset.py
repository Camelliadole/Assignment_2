import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
import PIL
import cv2
from matplotlib import pyplot as plt
from albumentations import (
    Compose, RandomBrightness, JpegCompression, HueSaturationValue, RandomContrast, HorizontalFlip,
    Rotate)
import albumentations as A
parent_dir = '/content/drive/MyDrive/Do Le Tra My/own_exactor_images'
store_dir = '/content/drive/MyDrive/Do Le Tra My/Augmentation'

if not os.path.exists(store_dir):
  os.makedirs(store_dir)
for fname in os.listdir(parent_dir):
  print("Processing " + fname + " ... ")
  img_path = os.path.join(parent_dir, fname) 
  store_path = os.path.join(store_dir, fname) 
  if not os.path.exists(store_path):
      os.makedirs(store_path)

  for filename in os.listdir(img_path):
        img = cv2.imread(os.path.join(img_path,filename))

        transform = A.Compose([
            Rotate(limit=40),
            RandomBrightness(limit=0.1),
            JpegCompression(quality_lower=85, quality_upper=100, p=0.5),
            HueSaturationValue(hue_shift_limit=20, sat_shift_limit=30, val_shift_limit=20, p=0.5),
            RandomContrast(limit=0.2, p=0.5),
            HorizontalFlip(),])
        image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        transformed = transform(image=image)
        transformed_image = transformed["image"]
        transformed_image.save(os.path.join(store_path , fname), "JPEG") #bug: 'numpy.ndarray' object has no attribute 'save'
