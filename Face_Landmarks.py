#
# 从一张图片中提取面部特征
#

import face_recognition
from PIL import Image, ImageDraw
#Python Image Library

marksDic= {
    "chin":"下巴",
    "left_eyebrow":"左眉毛",
    "right_eyebrow":"右眉毛",
    "nose_bridge":"鼻梁",
    "nose_tip":"鼻尖",
    "left_eye":"左眼",
    "right_eye":"右眼",
    "top_lip":"上嘴唇",
    "bottom_lip":"下嘴唇"
    }

print(marksDic.keys())

image = face_recognition.load_image_file("Images/obama.jpg")

#查找当前图片上所有人脸的所有面部特征
face_landmarks_list = face_recognition.face_landmarks(image)

print("我在这张图片中找到了{} 张人脸.".format(len(face_landmarks_list)))


#创建绘图对象
pil_image = Image.fromarray(image)
#draw = ImageDraw.Draw(pil_image)

for face_landmarks in face_landmarks_list:

    draw = ImageDraw.Draw(pil_image, 'RGBA')


    #打印面部特征的位置
    for facial_feature in face_landmarks.keys():

        print("{} 特征位于像素坐标点：{}".format(marksDic[facial_feature], face_landmarks[facial_feature]))

    
        # for facial_feature in face_landmarks.keys():
        #     draw.line(face_landmarks[facial_feature],width=5)

    draw.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
    draw.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
    draw.line(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 150), width=3)
    draw.line(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 150), width=3)

    draw.polygon(face_landmarks['top_lip'], fill=(150, 0, 0, 128))
    draw.polygon(face_landmarks['bottom_lip'], fill=(150, 0, 0, 128))
    draw.line(face_landmarks['top_lip'], fill=(150, 0, 0, 64), width=3)
    draw.line(face_landmarks['bottom_lip'], fill=(150, 0, 0, 64), width=3)

    draw.polygon(face_landmarks['left_eye'], fill=(255, 255, 255, 30))
    draw.polygon(face_landmarks['right_eye'], fill=(255, 255, 255, 30))

    draw.line(face_landmarks['left_eye'] + [face_landmarks['left_eye'][0]], fill=(0, 0, 0, 110), width=3)
    draw.line(face_landmarks['right_eye'] + [face_landmarks['right_eye'][0]], fill=(0, 0, 0, 110), width=3)


pil_image.show()

input()