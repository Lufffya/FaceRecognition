
#
# 读取Json文件图片地址下载图片
#

import os
import json
from urllib.request import urlretrieve


file = open("face_detection.json", "rb")
fileJson = json.load(file)

for index, item in enumerate(fileJson):
    try:
        urlretrieve(item["content"],"DataSet/images/"+str(index)+".jpg")
        print("下载第 {} 张".format(index))
    except Exception:
        continue

print()
