import cv2
import numpy as np
from math import ceil
import time
import copy


class faceManager:

	def __init__(self, cascade_file = "./cascades/haarcascade_frontalface_default.xml"):
		self.cascade =  cv2.CascadeClassifier(cascade_file)
		self.error_flag = False

	def detect_faces(self, image, threshold = 3):
		faces = self.cascade.detectMultiScale(image,1.3,threshold)
		return faces

	def preprocess_image(self, image):
		if not(isinstance(image, np.ndarray)):
			self.error_flag = True
			return None

		if (len(image.shape) > 2):
			output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		else:
			output = image

		return output

	def blur(self, image, intensity = 5):
		original_image = copy.deepcopy(image)
		target_image = self.preprocess_image(image)

		faces = self.detect_faces(target_image)

		for (x,y,w,h) in faces:
			shape = ceil(max(w,h)/intensity)
			if shape == 0:
				shape = 1
			kernel = np.ones((shape,shape), np.float32)/(shape*shape)

			if len(original_image.shape) > 2:
				for i in range(0,original_image.shape[2]):
					original_image[y:y+h, x:x+w, i] = cv2.filter2D(original_image[y:y+h, x:x+w, i], -1, kernel)
			else:
				original_image[y:y+h, x:x+w] = cv2.filter2D(original_image[y:y+h, x:x+w], -1, kernel)

		return original_image

	def pixelate(self, image):
		pass

	def draw(self, image, color=(0,255,0)):
		original_image = copy.deepcopy(image)
		target_image = self.preprocess_image(image)

		faces = self.detect_faces(target_image)

		for (x,y,w,h) in faces:
			original_image = cv2.rectangle(original_image, (x,y), (x+w,y+h), color, 1)

		return original_image