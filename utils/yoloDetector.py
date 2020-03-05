import cv2

import numpy as np

class yolov3Manager:
	def __init__(self, model_weights = "yolov3-tiny.weights", model_configuration = "yolov3-tiny.cfg", classes_file = "coco.names"):
		self.model_weights = model_weights
		self.model_configuration = model_configuration
		self.classes_file = classes_file

		self.net = cv2.dnn.readNetFromDarknet(model_configuration, model_weights)
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	def process_image(self, image, confidence_threshold = 0.5, nonmax_threshold = 0.4):
		# https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/

		output = self.get_output(image)

		chosen_classes = []
		confidences = []
		boxes = []

		image_height = image.shape[0]
		image_width = image.shape[1]

		for out in output:
			for detection in out:

				confidence = float(detection[4])
				if (confidence > confidence_threshold):

					chosen_class = np.argmax(detection[5:])
					center_x = int(detection[0] * image_width)
					center_y = int(detection[1] * image_height)


					width = max(0,int(detection[2] * image_width))
					height = max(0,int(detection[3] * image_height))
					x = max(0,int(center_x - (width/2)))
					y = max(0,int(center_y - (height/2)))
					
					chosen_classes.append(chosen_class)
					confidences.append(confidence)
					boxes.append([x, y, width, height])

		if len(confidences) != 0:
			indices = cv2.dnn.NMSBoxes(boxes, confidences, confidence_threshold, nonmax_threshold)
		else:
			return []

		retVal = []
		for i in indices:
			retVal.append(tuple(boxes[i[0]]))
		return retVal

	def get_output(self, image):

		image_height = 416#image.shape[0]
		image_width = 416#image.shape[1]

		blob = cv2.dnn.blobFromImage(image, 1/255,(image_width, image_height), [0,0,0], 1, crop=False)
		
		self.net.setInput(blob)

		output = self.net.forward(self.net.getUnconnectedOutLayersNames())
		return output