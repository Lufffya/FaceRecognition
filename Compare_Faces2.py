
#
# 从图片中识别人脸并标记她是谁
#

import face_recognition
from PIL import Image, ImageDraw
import numpy as np

# 这是在单个图像上运行人脸识别的示例
# 在每个被识别的人周围画一个盒子

# 加载示例图片并学习如何识别它
obama_image = face_recognition.load_image_file("Images/obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# 加载第二个示例图片并学习如何识别它
biden_image = face_recognition.load_image_file("Images/guyali.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# 创建已知面编码及其名称的数组
known_face_encodings = [

    obama_face_encoding,
    biden_face_encoding
]

known_face_names = [
    "Barack Obama",
    "Joe Biden"
]

# 加载带有未知面的图像
unknown_image = face_recognition.load_image_file("Images/timg (2).jpg")

# 在未知图像中找到所有的面部和脸部编码
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

# 将图像转换为PIL格式的图像，以便我们可以使用枕头库在其上绘制
# See http://pillow.readthedocs.io/ for more about PIL/Pillow
pil_image = Image.fromarray(unknown_image)
# 创建枕头ImageDraw绘图实例
draw = ImageDraw.Draw(pil_image)

# 遍历未知图像中的每个人脸
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # 查看该面是否与已知面匹配
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "不知道是谁"

    # 如果在已知的面编码中找到匹配项，请使用第一个
    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # 或者，使用与新面的距离最小的已知面
    # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    # best_match_index = np.argmin(face_distances)
    # if matches[best_match_index]:
    #     name = known_face_names[best_match_index]

    # 用枕头模块在脸上画一个盒子
    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    # 在面下画一个有名字的标签
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))


# 根据枕头文档从内存中删除绘图库
del draw

# 显示结果图像
pil_image.show()

# 如果需要，也可以通过取消注释此行将新图像的副本保存到磁盘
# pil_image.save("image_with_boxes.jpg")