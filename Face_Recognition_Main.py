#
# face_recognition 人脸识别函数封装
#

import os
import cv2
import numpy as np
import face_recognition
import matplotlib.pyplot as plt
from keras import backend as K
from keras.models import load_model
from PIL import Image,ImageDraw,ImageFont
import tensorflow as tf


class FaceRecognition():

    def SayHello(self=None):
        return "Hello Python Flask dfsdsdsdsd"

    def Find_Face(fileName):

        image = face_recognition.load_image_file("static/images/"+fileName)

        face_locations = face_recognition.face_locations(image)

        # 使用卷积神经网络深度学习模型定位人脸
        if len(face_locations) == 0:
            face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

        for index in range(len(face_locations)):
            top, right, bottom, left = face_locations[index]

            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            title="face"+str(index+1)

            #计算矩阵
            subIndex = 1
            while ((len(face_locations)) / subIndex) > subIndex :
                subIndex += 1

            #行,列,索引
            plt.subplot(subIndex,subIndex,index+1)
            plt.imshow(pil_image)
            plt.title(title,fontsize=8)
            plt.axis('off')
        fileName = fileName+ "_Recognition.jpg"
        plt.savefig('static/save_Images/'+fileName)
        plt.clf()
        return fileName

    def Face_Recognition(file_Name):
        #存已识别的名称
        Names = []
        #存图片
        array_of_img = []
        #存图片中人脸的名称
        array_of_face_Name = []
        #存人脸的面部编码
        array_of_face_encoding = []

        #获取指定文件下的所有图片
        for filename in os.listdir("Compare_Faces_Images"):

            img = face_recognition.load_image_file("Compare_Faces_Images/" + filename)
            array_of_img.append(img)

            filename = os.path.splitext(filename)
            array_of_face_Name.append(filename[0])

        #获取对应图片的面部编码
        for image in array_of_img:
            try:
                face_encoding = face_recognition.face_encodings(image)[0]
                array_of_face_encoding.append(face_encoding)
            except Exception :
                continue

        # 加载带有未知面的图像
        unknown_image = face_recognition.load_image_file("static/images/"+file_Name)
        unknown_face_encodings = []

        try:
            # 在未知图像中找到所有的面部和脸部编码
            face_locations = face_recognition.face_locations(unknown_image)
            unknown_face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

            print(unknown_face_encodings)

        except Exception :
            return "从上传的图片中找不到任何人脸"

        for face_encoding in unknown_face_encodings:

            # 从已知的面部编码中匹配未知的面部编码
            matches = face_recognition.compare_faces(array_of_face_encoding, face_encoding)
            name = "张三"

            # 如果在已知的面编码中找到匹配项，请使用第一个
            #if True in matches:
            #    first_match_index = matches.index(True)
            #    name = array_of_face_Name[first_match_index]
            #else:
            # 或者，使用与新面的距离最小的已知面
            face_distances = face_recognition.face_distance(array_of_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = array_of_face_Name[best_match_index]
                    
            Names.append(name)
        
        return Names
    
    def Gender_Recognition(fileName):

        print("static/images/"+fileName)

        Names = []
        #opencv 读取图片
        img = cv2.imread("static/images/"+fileName)
        # CascadeClassifier opencv级联分类器 作用：人脸检测
        face_classifier = cv2.CascadeClassifier("Gender_Models/haarcascade_frontalface_default.xml")
        # COLOR_BGR2GRAY 将图片灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # scaleFactor：表示每次图像尺寸减小的比例
        # minNeighbors: 检测次数
        # minSize：图片的最小尺寸
        # detectMultiScale ：opencv训练好的模型
        faces = face_classifier.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3,minSize=(140, 140))
        #face_locations = face_recognition.face_locations(gray)
        
        K.clear_session()
        # 导入性别识别模型
        gender_classifier = load_model("Gender_Models/simple_CNN.81-0.96.hdf5")
        # 定义性别
        gender_labels = {0: '女', 1: '男'}
        color = (255, 255, 255)
        for (x, y, w, h) in faces:
        #for index, (top, right, bottom, left) in enumerate(face_locations): 
            try:
                face = img[(y - 60):(y + h + 60), (x - 30):(x + w + 30)]
                #face = img[(right - 60):(right + left + 60), (top - 30):(top + bottom + 30)]
                face = cv2.resize(face, (48, 48))
                face = np.expand_dims(face, 0)
                face = face / 255.0
                gender_label_arg = np.argmax(gender_classifier.predict(face))
                # 匹配性别
                gender = gender_labels[gender_label_arg]
                Names.append(gender)
            except Exception as e:
                Names.append("未知")
                
        return Names