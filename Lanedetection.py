import cv2
import numpy as np
import time

def resize_crop_frame(image, desired_x, crop_ratio):
	
	size = image.shape
	cropped_image = image[100: size[0], 0:size[1]]

	return cropped_image

def image_changes(image):


	edit_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	unsharp_image = cv2.addWeighted(edit_image, 1.5, edit_image, -0.5, 0, edit_image)

	thresh = 240

	edit_image = cv2.threshold(edit_image, thresh, 255, cv2.THRESH_BINARY)[1]

	edit_image = cv2.dilate(edit_image, (7,7))

	#cv2.imshow("thresh", edit_image)

	#edit_image = cv2.Canny(edit_image,200,400)

	#edit_image = cv2.GaussianBlur(edit_image, (3,3), 0 )



	return edit_image

def find_lines(image, draw_image):

	lines = cv2.HoughLinesP(image, 1, np.pi/180, 180, np.array([]) , 5, 5)
	lines_to_return = []

	try:

		for line in lines:
			coords = line[0]
			#print(coords)

			x1=int(coords[0])
			x2=int(coords[2])
			y1=int(coords[1])
			y2=int(coords[3])

			slopex = x2-x1
			slopey = y2-y1

			if slopey != 0:
				slope = float(slopex)/float(slopey)
			else:
				slope = 100

			#print(slopey,slopex,slope)

			x = (x2-x1)**2
			y = (y2-y1)**2
			z = int(x + y)
			length = int(z**(1/2.0))

			#print(slope, length)

			if length > int(10):
				if slope < int(1):
					if slope > int(-1):
						lines_to_return += [[x1, y1, x2, y2, slope, length]]
						cv2.line(draw_image, (x1,y1), (x2,y2), [255,255,0], 3)

		return lines_to_return

	except:
		return [[0,0,0,0,0,0]]


def line_grouping(line_list):

	
	list_negtwo = list()
	list_negone = list()
	list_zero = list()
	list_posone = list()
	list_postwo = list()
	

	for i in range(len(line_listt)):
		line = line_list[i]
		slope = line[4]
		if slope == -2:
			list_negtwo.append(line)

		if slope == -1:
			list_negone.append(line)

		if slope == 0:
			list_zero.append(line)

		if slope == 1:
			list_posone.append(line)

		if slope == 2:
			list_postwo.append(line)


	grouped_list = list()
	grouped_list.append(list_negtwo)
	grouped_list.append(list_negone)
	grouped_list.append(list_zero)
	grouped_list.append(list_posone)
	grouped_list.append(list_postwo)

	return grouped_list


def create_single_line(list_of_lines):

	x1_sum = 0
	x2_sum = 0
	y1_sum = 0
	y2_sum = 0

	length_of_list = len(list_of_lines)

	for i in range(length_of_list):
		x1_sum += list_of_lines[i][0]
		x2_sum += list_of_lines[i][2]
		y1_sum += list_of_lines[i][1]
		y2_sum += list_of_lines[i][3]

	x1_mean = int(x1_sum / length_of_list)
	x2_mean = int(x2_sum / length_of_list)
	y1_mean = int(y1_sum / length_of_list)
	y2_mean = int(y2_sum / length_of_list)

	
	x1 = x1_mean
	x2 = x2_mean
	y1 = y1_mean
	y2 = y2_mean


	single_line = (x1, y1, x2, y2)

	return single_line

    

def draw_single_lines(grouped_list, draw_image):

	for i in range(5):

		if len(grouped_list[i]) > 3:
			single_line = create_single_line(grouped_list[i])
			cv2.line(draw_image, (single_line[0],single_line[1]), (single_line[2],single_line[3]), [0,255,255], 3)


def BirdsEyeView(image):

	image = cv2.resize(image, (1280, 720))
	
	mage = image[0:600, 220:1280]

	image = cv2.resize(image, (1280, 720))

	img_size = (1000, 480)

	src = np.float32([[0, 600], [1280, 600], [0, 400], [1280, 400]])

	dst = np.float32([[390, 500], [610, 500], [-180, -50], [1180, -50]])


	M = cv2.getPerspectiveTransform(src, dst)

	Minv = cv2.getPerspectiveTransform(dst, src)

	warped = cv2.warpPerspective(image, M, img_size)

	return warped



def lane_line_detect(image):

	BirdeyeImage = BirdsEyeView(image)

	edit_image = image_changes(BirdeyeImage)

	#line_list = find_lines(edit_image, BirdeyeImage)

	#grouped_list = line_grouping(line_list)

	#draw_single_lines(grouped_list, cropped_image)

	return edit_image




def main():

	crop_ratio = 0.55
	desired_x = 1024

	video = cv2.VideoCapture('FNTestCenter.mp4')

	while True:

		start = time.clock()

		flag, image = video.read()


		#image = resize_crop_frame(image, desired_x, crop_ratio)

		cv2.imshow("normal", image)

		BirdeyeImage = BirdsEyeView(image)

		#time_elapsed = time.clock() - start

		#print("Read in:", time_elapsed)

		#cropped_image = resize_crop_frame(image, desired_x, crop_ratio)

		#time_elapsed = time.clock() - start

		#print("Cropped in:", time_elapsed)

		#if not flag:
		#	break


		edit_image = lane_line_detect(image)
		'''

		edit_image = image_changes(BirdeyeImage)


		cv2.imshow("edit", edit_image)

		#cv2.imshow("edited", edit_image)

		#time_elapsed = time.clock() - start

		#print("Edited in:", time_elapsed)

		line_list = find_lines(edit_image, BirdeyeImage)

		#time_elapsed = time.clock() - start

		#print("Found lines in:", time_elapsed)

		#grouped_list = line_grouping(line_list)

		#time_elapsed = time.clock() - start

		#print("Grouped in:", time_elapsed)

		#draw_single_lines(grouped_list, cropped_image)

		'''

		
		

		cv2.imshow("Edit", BirdeyeImage)

		cv2.imshow("Edit2", edit_image)
		cv2.waitKey(10)

		#time_elapsed = time.clock() - start

		#print("Total:", time_elapsed)



if True:
	main()

