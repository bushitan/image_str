#--coding:utf-8--
# import cv2
# import numpy as np
#
# url = r'E:\Carcer World\code\Python\git\image_str\image_server\grid\static\art\img\20160808114358.png'
# img = cv2.imread(url, 0)
#
# img = cv2.GaussianBlur(img,(3,3),0)
# canny = cv2.Canny(img, 50, 150)
#
# # cv2.imshow('Canny', canny)
# cv2.imshow('Canny', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


''' file name : canny.py
Description : This sample shows how to find edges using canny edge detection
This is Python version of this tutorial : http://opencv.itseez.com/doc/tutorials/imgproc/imgtrans/canny_detector/canny_detector.html
Level : Beginner
Benefits : Learn to apply canny edge detection to images.
Usage : python canny.py
Written by : Abid K. (abidrahman2@gmail.com) , Visit opencvpython.blogspot.com for more tutorials '''


import cv2
import numpy as np
import time
def CannyThreshold(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray,(9,9),0) # （ 5,5 ）为高斯核的大小， 0 为标准差
    detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)

    # print detected_edges

    dst = cv2.bitwise_and(img,img,mask = detected_edges)  # 遮罩层，就是镂空的 just add some colours to edges from original image.

    # iTmp = cv2.CreateImage(size,image.depth,image.nChannels)

    # iTmp=np.zeros(detected_edges.shape, np.uint8)
    #
    # print detected_edges.shape
    # for i in range(detected_edges.shape[0]):
    #     for j in range(detected_edges.shape[1]):
    #         iTmp[i,j] = 255 - detected_edges[i,j]

    cv2.imshow('canny demo',detected_edges)

    _img_filedir = "art/"
    _img_name = "{}".format(time.strftime('%Y%m%d%H%M%S'))
    _img_style = ".png"
    _img_filename = _img_name+_img_style
    _img_localpath = _img_filedir + _img_filename
    cv2.imwrite(_img_localpath, detected_edges, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])
    # cv2.imwrite("cat.png", dst, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

lowThreshold = 0
max_lowThreshold = 100
ratio = 3
kernel_size = 3

name = '20160808114358.png'

url = r'C:\Users\Administrator\Desktop\30day\xiangao\10.jpg'
url_mm_tx = r'C:\Users\Administrator\Desktop\30day\learn\3.jpg'

img = cv2.imread(url_mm_tx)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


cv2.namedWindow('canny demo')

cv2.createTrackbar('Min threshold','canny demo',lowThreshold, max_lowThreshold, CannyThreshold)

CannyThreshold(20)  # initialization

if cv2.waitKey(0) == 27:
    cv2.destroyAellWindows()
