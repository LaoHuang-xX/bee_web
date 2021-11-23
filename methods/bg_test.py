import cv2
import pathlib as path
import argparse
import numpy as np

file_suffix = '.jpg'
count = 0

fgbg = cv2.createBackgroundSubtractorMOG2()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

while count < 3:
    dir_file = str(count) + file_suffix
    cap = cv2.imread(dir_file)
    ret, frame = cv2.threshold(cap, 127, 255, cv2.THRESH_BINARY)

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    cv2.imshow('frame', fgmask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    count += 1

cv2.waitKey(0)
cv2.destroyAllWindows()



################################### Old Version ################################
# #
# # read image as greyscale
# img_1 = cv2.imread('bg_test.jpg')
#
# cv2.imshow("Binary Image", img_1)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# img_1 = cv2.imread('bg_test.jpg', 2)
#
# cv2.imshow("Binary Image", img_1)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# ret, img_1 = cv2.threshold(img_1,127,255,cv2.THRESH_BINARY)
#
# cv2.imshow("Binary Image", img_1)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# img_2 = cv2.imread('bg_test_1.jpg')
#
# cv2.imshow("Binary Image", img_2)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# img_2 = cv2.imread('bg_test_1.jpg', 2)
#
# ret, img_2 = cv2.threshold(img_2,127,255,cv2.THRESH_BINARY)
#
# cv2.imshow("Binary Image", img_2)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# labels = np.zeros(img_2.shape)
# label = 1.0
# record = {}
#
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         if img_1[i][j] == img_2[i][j]:
#             img_2[i][j] = 255
#         if img_2[i][j] == 0:
#             if i > 0 and labels[i - 1][j] != 0:
#                 labels[i][j] = labels[i - 1][j]
#                 record[str(labels[i][j])] += 1
#             elif j > 0 and labels[i][j - 1] != 0:
#                 labels[i][j] = labels[i][j - 1]
#                 tmp = record[str(labels[i][j])]
#                 record[str(labels[i][j])] = tmp + 1
#             else:
#                 labels[i][j] = label
#                 record[str(label)] = 1
#                 label += 1
#
# cv2.imshow("Binary Image", img_2)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# for i in range(img_2.shape[0]):
#     for j in range(img_2.shape[1]):
#         if labels[i][j] != 0 and record[str(labels[i][j])] < 30:
#             img_2[i][j] = 255
#
# cv2.imshow("Binary Image", img_2)
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()



