#
# 从一张图片中定位人脸的位置
#

import face_recognition
from PIL import Image

import matplotlib.pyplot as plt

image = face_recognition.load_image_file("Images/sucai.jpg")

face_locations = face_recognition.face_locations(image)

# 使用卷积神经网络深度学习模型定位人脸
#face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0, model="cnn")

print("在当前图片中共找到 {} 张人脸".format(len(face_locations)))

for index in range(len(face_locations)):
    top, right, bottom, left = face_locations[index]
    print("第 {} 张人脸位于像素位置 顶部: {}, 左边: {}, 底部: {}, 右边: {}".format(index,top, left, bottom, right))
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    
    title="face"+str(index+1)
    #行,列,索引

    subIndex = 1

    while ((len(face_locations)) / subIndex) > subIndex :
        subIndex += 1

    plt.subplot(subIndex,subIndex,index+1)
    plt.imshow(pil_image)
    plt.title(title,fontsize=10)
    plt.axis('off')

    #pil_image.show()
    #pil_image.save("Save_Img_Demo/obama"+str(index)+".jpg")

plt.show()

input()
