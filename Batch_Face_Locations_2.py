#
# 使用卷积神经网络深度学习模型批量识别图片中的人脸
#

import face_recognition
import cv2

from PIL import Image
import matplotlib.pyplot as plt

# 从文件从读取视频资源
video_capture = cv2.VideoCapture("Videos/QQ123.mp4")

# 表示每一帧的图像数据
frames = []
# 帧计数,表示读取帧的次数
frame_count = 0

# isOpened() -> Bool 如果视频资源已加载成功返回True
while video_capture.isOpened():

    # read() 表示按帧读取视频
    # ret -> Bool 表示真否读取到正确的帧
    # frame -> 三维矩阵 表示每一帧的图像
    ret, frame = video_capture.read()

    # 视频文件结束时跳出
    if not ret:
        break

    cv2.imshow("frameImage", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Opencv 读取图片默认像素排列是BGR
    # Face_Recognition 处理像素采用通用格式RGB
    # 将图像从bgr颜色转换为rgb颜色
    frame = frame[:, :, ::-1]

    # 将视频的每帧图像保存到列表中
    frame_count += 1
    frames.append(frame)

    # 每128帧（默认批处理大小），批处理要查找面的帧列表
    if len(frames) == 2:
        batch_of_face_locations = face_recognition.batch_face_locations(frames,number_of_times_to_upsample=0,batch_size=2)

        for frame_number_in_batch, face_locations in enumerate(batch_of_face_locations):
            number_of_faces_in_frame = len(face_locations)

            frame_number = frame_count - 2 + frame_number_in_batch
            print("在第 {} 帧中找到 {} 张人脸".format(frame_number,number_of_faces_in_frame))

            image =frames[frame_number_in_batch]

            for index,face_location in enumerate(face_locations):
                top, right, bottom, left = face_location
                print("人脸位于像素位置 顶部: {}, 左边: {}, 底部: {}, 右边: {}".format(top, left, bottom, right))

                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)
                title="face"+str(index+1)
                #行,列,索引
                plt.subplot(3,3,index+1)
                plt.imshow(pil_image)
                plt.title(title,fontsize=10)
                plt.axis('off')

            plt.show()  

        # 清除“帧”数组以开始下一组
        frames = []

input()