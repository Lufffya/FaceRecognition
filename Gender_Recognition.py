
#coding=utf-8
#性别识别

import face_recognition
import cv2
from keras.models import load_model
import numpy as np
#import ChineseText
from PIL import Image

#coding=utf-8
#中文乱码处理

from PIL import Image, ImageDraw, ImageFont

def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)):  #判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype("font/simsun.ttc", textSize, encoding="utf-8")
    draw.text((left, top), text, textColor, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


img = cv2.imread("static/Images/zhanghan.jpg")

face_classifier = cv2.CascadeClassifier("Gender_Models/haarcascade_frontalface_default.xml")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow("Image", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cv2.imshow("CV_BGR2GRAY转换后",gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

faces = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3, minSize=(140, 140))

gender_classifier = load_model("Gender_Models/simple_CNN.81-0.96.hdf5")
gender_labels = {0: '女', 1: '男'}
color = (255, 255, 255)


face_locations = face_recognition.face_locations(gray)

# top, right, bottom, left = face_locations[index]
# print("第 {} 张人脸位于像素位置 顶部: {}, 左边: {}, 底部: {}, 右边: {}".format(index,top, left, bottom, right))
# face_image = image[top:bottom, left:right]
# pil_image = Image.fromarray(face_image)


for index, (top, right, bottom, left) in enumerate(face_locations):  
    face = img[top:bottom, left:right]
    face = img[(right - 60):(right + left + 60), (top - 30):(top + bottom + 30)]
    face = cv2.resize(face, (48, 48))
    face = np.expand_dims(face, 0)
    face = face / 255.0
    #pil_image = img.fromarray(face)
    #pil_image.show()
    # face = cv2.resize(face, (48, 48))
    # face = np.expand_dims(face, 0)
    # face = face / 255.0
    gender_label_arg = np.argmax(gender_classifier.predict(face))
    gender = gender_labels[gender_label_arg]
    #cv2.rectangle(img, (top, right), (top + left, right + bottom), color, 2)
    #img = cv2ImgAddText(img, gender, top + left, right, color, 30)


# for (x, y, w, h) in faces:
#     face = img[(y - 60):(y + h + 60), (x - 30):(x + w + 30)]
#     face = cv2.resize(face, (48, 48))
#     face = np.expand_dims(face, 0)
#     face = face / 255.0
#     gender_label_arg = np.argmax(gender_classifier.predict(face))
#     gender = gender_labels[gender_label_arg]
#     cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
#     img = cv2ImgAddText(img, gender, x + h, y, color, 30)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()