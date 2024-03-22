# -*- coding: utf-8 -*-
"""Slash AI Task Final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rTrv9ANGhHzsQV8_qFUSD2VJJYUKYn7C

##Image Classfier Model for Slash##

##Outlines

1. Dataset Download:
2. Data Preparation
3. Model Building
4. Training
5. Validation
6. Fine-Tuning
7. Testing

##Imports
"""

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.applications import MobileNetV2
from sklearn.model_selection import KFold
import cv2
import os

from google.colab import drive
drive.mount('/content/drive')

"""##Data Collection

Data is collected from Slash Application, with good quality. Here I'll show sample from the data labeled for training.
"""

import os
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt  # Choose matplotlib for image display

# Assuming your Google Drive is already mounted at /content/drive
train_dir = '/content/drive/MyDrive/Data'  # Replace with the actual path
val_dir = '/content/drive/MyDrive/Validation'
#test_dir = '/content/drive/MyDrive/Test'

try:
    class_folders = sorted(os.listdir(train_dir))
except FileNotFoundError:
    print("Error: The specified base directory does not exist. Please check the path.")
    raise

# Display 1 sample image per class
num_samples_per_class = 1

for class_folder in class_folders:
    label = class_folder
    class_folder_path = os.path.join(train_dir, class_folder)
    image_files = [
        os.path.join(class_folder_path, img)
        for img in os.listdir(class_folder_path)
        if img.endswith((".jpg", ".png", ".jpeg"))
    ]

    print(f"Class: {label}")

    for i in range(min(num_samples_per_class, len(image_files))):
        image_size = load_img(image_files[i], target_size=(224, 224)) ##resize>Preparation
        img_array = img_to_array(image_size) / 255.0  # Normalize for display >Preparation

        plt.imshow(img_array)
        plt.title(f"{label} - {image_files[i].split('/')[-1]}")
        plt.axis('off')
        plt.show()

print("Done displaying sample images!")

"""##Data Prepartions

Here data undergoes prepartion phase by normalzing the images, resizing, and data agumentation due to dataset limited size.
"""

# K-Fold parameters
n_splits = 5  # Adjust as needed (e.g., 3 or 10)
image_size = (224, 224)
batch_size = 16
# Data augmentation parameters (adjust as needed)
data_augmentation = dict(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True
)

# Define KFold object
kfold = KFold(n_splits=n_splits, shuffle=True)

# Loop through each fold for K-Fold cross-validation
for train_index, val_index in kfold.split(os.listdir(train_dir)):

  # Define training and validation data paths based on indices
  train_data_paths = [os.path.join(train_dir, f) for f in os.listdir(train_dir) if f in train_index]
  val_data_paths = [os.path.join(train_dir, f) for f in os.listdir(train_dir) if f in val_index]

  # Create data generators with augmentation for training and no augmentation for validation
  train_datagen = ImageDataGenerator(**data_augmentation)
  train_generator = train_datagen.flow_from_directory(
      train_dir,
      target_size=image_size,
      batch_size=batch_size,
      class_mode='categorical'
  )

  val_datagen = ImageDataGenerator(rescale=1./255)
  validation_generator = val_datagen.flow_from_directory(
      val_dir,
      target_size=image_size,
      batch_size=batch_size,
      class_mode='categorical'
  )

"""##Model Building - Model Training - Model Validation

Here is model building and training phase, by using pre-built model MobileNetV2. This pre-built model is used due to limtted data size, so any model from scartch would be too complex for the dataset.
"""

# Build the model
model = Sequential()
model.add(MobileNetV2(input_shape=(image_size[0], image_size[1], 3), weights='imagenet', include_top=False))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

model.compile(optimizer=Adam(lr=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

  # Early stopping callback
#early_stopping = EarlyStopping(monitor='val_loss', patience=3)

  # Train the model
model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=20,  # Adjust as needed
    validation_data=validation_generator,
    validation_steps=len(validation_generator)
    #callbacks=[early_stopping]
  )

"""##Model Testing"""



"""##Resources

1.   https://stackoverflow.com/questions/68240952/invalidargumenterror-conv2dbackpropfilter-input-depth-must-be-evenly-divisible
2.   https://stackoverflow.com/questions/54896938/syntax-difference-for-programming-with-and-without-gpu

1.   https://github.com/AndreiXYZ/licenta

1.   https://github.com/gaborpelesz/openai_caribbean
2.   https://github.com/hc07180011/mds-2021

1.   https://sailajakarra.medium.com/deep-learning-using-tensorflow-part3-9c16434b379c
"""