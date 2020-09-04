#
# 自定义数据集的图片分类
# 

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
import cv2
import os
from PIL import Image

def preprocess_image(image):
  image = tf.image.decode_jpeg(image, channels=3)
  image = tf.image.resize(image, [192, 192])
  image /= 255.0  # normalize to [0,1] range
  return image

def load_and_preprocess_image(path):
  image = tf.io.read_file(path)
  return preprocess_image(image)

import IPython.display as display
def caption_image(image_path):
    image_rel = pathlib.Path(image_path).relative_to(data_root)
    return "Image (CC BY 2.0) " + ' - '.join(attributions[str(image_rel)].split(' - ')[:-1])

#标签分类
mySelf_className= ["存在人脸","不存在人脸"]

# 用于训练的数据
train_images = []
# 用于训练的标签
train_labels =[]

# 用于测试的数据
test_images = []
# 用于测试的标签
test_labels = []

# 存在人脸的图片路径
for index,filename in enumerate(os.listdir("DataSet/images/")):
    img = cv2.imread("DataSet/images/" + filename)[:,:,::-1]

    # tf 原始数据
    #img_raw = tf.io.read_file("DataSet/images/" + filename)
    # 解码为图像 tensor
    #img_tensor = tf.image.decode_image(img_raw)

    # cv2.imshow("1",img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 缩小图像  
    size = (int(300), int(300))  
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  

    #image = tf.image.resize(img,)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img / 255.0

    if index > 310 :
        test_images.append(img)                        
        test_labels.append(1)
        
    else:# 添加训练人脸图片
        train_images.append(img)
        train_labels.append(1)

# 不存在人脸的图片路径
for index,filename in enumerate(os.listdir("DataSet/Scenery/")):
    img = cv2.imread("DataSet/Scenery/" + filename)[:,:,::-1]
    #img_raw = tf.io.read_file("DataSet/Scenery/" + filename)


    #img = tf.image.resize(img, [192, 192]) 
    size = (int(300), int(300))  
    img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)  

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)              
    img = img / 255.0

    if index > 310 :
        test_images.append(img)
        test_labels.append(0)
    else:# 添加训练风景图片
        train_images.append(img)
        train_labels.append(0)

# index = [i for i in range(len(train_images))]  
# random.shuffle(index)

# train_images = train_images[index]
# train_labels = train_labels[index]

#train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels))
#test_dataset = tf.data.Dataset.from_tensor_slices((test_images, test_labels))

train_images = np.array(train_images,dtype=float)

train_labels = np.array(train_labels)


test_images = np.array(test_images,dtype=float)

test_labels = np.array(test_labels)


model = keras.Sequential()
#[300*300,1]
model.add(keras.layers.Reshape([300,300,1]))
model.add(keras.layers.Conv2D(32, (3, 3)))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D())
model.add(keras.layers.Dropout(0.2))
model.add(keras.layers.Conv2D(32, (3, 3)))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D())
model.add(keras.layers.Dropout(0.2))

model.add(keras.layers.Conv2D(64, (3, 3)))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.MaxPooling2D())
model.add(keras.layers.Dropout(0.2))

model.add(keras.layers.Flatten())
model.add(keras.layers.Dense(64))
model.add(keras.layers.Activation('relu'))
model.add(keras.layers.Dense(1))
model.add(keras.layers.Activation('sigmoid'))

# 创建模型

# model = keras.Sequential({
#     keras.layers.Flatten(),
#     keras.layers.Dense(128, activation='relu'),
#     keras.layers.Dense(32, activation='relu'),
#     keras.layers.Dense(1, activation='sigmoid')})

# 编译模型
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

# 训练模型
model.fit(train_images, train_labels, epochs=20,validation_data=(test_images, test_labels))
#steps_per_epoch=1

# 验证
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)