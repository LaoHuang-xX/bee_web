'''
Xu Hai Feb 5 2022
Python program to build the video based on images
'''

import pickle
import cv2
import os
import numpy as np


# Read the pickle file
# Names should be changed for different files
infile = open('2021-08-30-09-28-39.html_top', 'rb')
new_dict_top = pickle.load(infile)

infile_side = open('2021-08-30-09-28-39.html_side', 'rb')
new_dict_side = pickle.load(infile_side)

print(new_dict_top)
print(new_dict_side)

black_image = cv2.imread(os.getcwd() + '/data/' + 'black.jpg')

img_list = []

# Match corresponding top view and side view images
# And merge them into vertical format
for i in new_dict_top:
    min_len = min(len(new_dict_side[i]), len(new_dict_top[i]))
    for j in range(min_len):
        img1 = cv2.imread(os.getcwd() + '/data/' + new_dict_side[i][j])
        img2 = cv2.imread(os.getcwd() + '/data/' + new_dict_top[i][j])
        ver = np.vstack((img1, img2))
        img_list.append(ver)

height, width, layers = img_list[0].shape
size = (width, height)

out = cv2.VideoWriter('video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)

# Write each frame of the video
for img in img_list:
    out.write(img)

out.release()
