import cv2
import numpy as np
import time


def BirdsEyeView(image):

	image = cv2.resize(image, (1280, 620))

	img_size = (1000, 500)

	src = np.float32([[0, 600], [1280, 600], [0, 390], [1280, 390]])

	dst = np.float32([[420, 500], [580, 500], [-160, -50], [1330, -50]])

	M = cv2.getPerspectiveTransform(src, dst)

	Minv = cv2.getPerspectiveTransform(dst, src)

	warped = cv2.warpPerspective(image, M, img_size)

	return warped

image = cv2.imread('FNscreenshotCenter.png')


image = cv2.resize(image, (1280, 720))

image = image[0:600, 220:1280]

warped = BirdsEyeView(image)

image = cv2.resize(image, (640, 360))


cv2.imshow("normal", image)

cv2.imshow("warped", warped)

cv2.waitKey(100000)