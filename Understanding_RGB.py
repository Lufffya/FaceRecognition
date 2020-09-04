#
# 理解RGB概念
#

import cv2

def access_pixels(frame):
    print(frame.shape)  #shape内包含三个元素：按顺序为高、宽、通道数
    height = frame.shape[0]
    width = frame.shape[1]
    channels = frame.shape[2]
    print("width : %s, height : %s, channel : %s" %(width, height, channels))

    for row in range(height):            #遍历高
        for col in range(width):         #遍历宽
            for c in range(channels):     #便利通道
                pv = frame[row, col, c]
                frame[row, col, c] = 255 - pv     #全部像素取反，实现一个反向效果
    cv2.imshow("new", frame)


if __name__ == "__main__":
    image = "Images/obama.jpg"
    src = cv2.imread(image)
    cv2.imshow("old", src)
    access_pixels(src)
    cv2.waitKey()
