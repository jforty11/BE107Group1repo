#!/usr/bin/python
import numpy as np  # Presumably something to do with numbers
import cv2          # Image processing
from matplotlib import pyplot as plt # Plotting function or something

directory = "/home/lev/Documents/College/Be107/Week5/videos_for_tracking/larvae_stills/"
prefix = "frame000"
suffix = ".jpg"
infix = [0, 1, 2, 3, 4, 5, 6, 7]
img = cv2.imread(directory + prefix + str(infix[6]) + suffix, cv2.IMREAD_GRAYSCALE)
print(directory + prefix + str(infix[6]) + suffix)

# What are the dimensions of the image?
print img

# Invert image
img = 255 - img
img2 = img # Copy

# Threshold image -- might be better to use THRESH_TRUNC
ret, thresh = cv2.threshold(img, 50, 255, cv2.THRESH_TOZERO_INV)
#cv2.imshow('Regular thresholding', thresh)

# Threshold with adaptive thresholding
thresh2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19, 8)
#cv2.imshow('Adaptive thresholding', thresh2)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


contour_mean = []
for i, e in enumerate(contours):
  cont_x=[]
  cont_y=[]
  for i2, val in enumerate(e):
    for i3, val2 in enumerate(val):
      #print(e)
      cont_x.append(val2[0])
      cont_y.append(val2[1])
  cont_mean = [np.mean(cont_x), np.mean(cont_y)]
  contour_mean.append(cont_mean)




#print contours
#cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
#cv2.drawContours(img2, contours2, -1, (0, 255, 0), 3)

#cv2.imshow('dis image doe', img)
#cv2.imshow('dis inmage doeeee', img2)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Accumulate weighted
total_img = np.zeros((480, 752))

for x in infix:
    img = cv2.imread(directory + prefix + str(x) + suffix, cv2.IMREAD_GRAYSCALE)
    cv2.accumulateWeighted(img, total_img, 0.1)

# If we want to dispaly total_img we have to divide by 255 since float types are assumed to scale from 0 to 1 rather than 0 to 255
#total_img /= 255
#cv2.imshow('dat booty and we call her', total_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

for x in infix:
    img = cv2.imread(directory + prefix + str(x) + suffix, cv2.IMREAD_GRAYSCALE)
    img = cv2.absdiff(img, total_img.astype('uint8'))

    img = 255 - img

    ret, thresh = cv2.threshold(img, 175, 255, cv2.THRESH_TOZERO_INV)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    contour_mean = []
    for i, e in enumerate(contours):
      cont_x=[]
      cont_y=[]
      for i2, val in enumerate(e):
	for i3, val2 in enumerate(val):
	  #print(e)
	  cont_x.append(val2[0])
	  cont_y.append(val2[1])
      cont_mean = [np.mean(cont_x), np.mean(cont_y)]
      contour_mean.append(cont_mean)
    for circ, cval in enumerate(contour_mean):
      cv2.circle(img, (int(cval[0]),int(cval[1])), 8, 'red')

    cv2.imshow('dflickoooo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
