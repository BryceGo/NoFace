import cv2
import numpy as np
from math import ceil

def main(file_name):
	classifier = cv2.CascadeClassifier("./cascades/haarcascade_frontalface_default.xml")
	img = cv2.cvtColor(cv2.imread(file_name), cv2.COLOR_BGR2GRAY)

	faces = classifier.detectMultiScale(img, 1.3, 3)

	for (x,y,w,h) in faces:
		shape = ceil(max(w,h)/5)
		if shape == 0:
			shape = 1


		kernel = np.ones((shape,shape), np.float32)/(shape*shape)
		img[y:y+h, x:x+w] = cv2.filter2D(img[y:y+h, x:x+w], -1, kernel)


	cv2.imshow('img', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main(".\\images\\test.png")
