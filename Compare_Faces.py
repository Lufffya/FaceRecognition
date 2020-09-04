
#
# 对比人脸,从已的人脸中匹配未知人脸
#

import face_recognition


biden_image = face_recognition.load_image_file("Images/obama2.jpg")
obama_image = face_recognition.load_image_file("Images/biden.jpg")
unknown_image = face_recognition.load_image_file("Images/baby.png")


# 获取每个图像文件中每个面的面编码
# 因为每个图像中可能有多个面，所以它返回一个编码列表
# 但是由于我知道每个图像只有一个面，所以我只关心每个图像中的第一个编码，所以我获取索引 0
try:
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

except IndexError:
    print("找不到任何人脸")
    quit()

known_faces = [
    biden_face_encoding,
    obama_face_encoding
]

# 结果是一个判断未知人脸是否与已知人脸数组中的任何人匹配的真/假数组
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)


print("是奥巴马吗? {}".format(results[0]))
print("是古丽亚吗? {}".format(results[1]))
print("未知的面孔是我们从未见过的面孔吗? {}".format(not True in results))