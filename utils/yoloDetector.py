class yolov3Manager:
	def __init__(self, model_weights = "yolov3.weights", model_configuration = "yolov3.cfg", classes_file = "coco.names"):
		self.model_weights = model_weights
		self.model_configuration = model_configuration
		self.classes_file = classes_file

		self.net = cv2.dnn.readNetFromDarknet(model_configuration, model_weights)
		self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
		self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

	def process_image(self, image, confidence_threshold = 0.4):
		output = self.get_output(image)
		# Add Non-max implementation here
		# https://www.learnopencv.com/deep-learning-based-object-detection-using-yolov3-with-opencv-python-c/


	def get_output(self, image):

		image_height = 416#image.shape[0]
		image_width = 416#image.shape[1]

		blob = cv2.dnn.blobFromImage(image, 1/255,(image_width, image_height), [0,0,0], 1, crop=False)
		
		self.net.setInput(blob)

		output = self.net.forward(self.net.getUnconnectedOutLayersNames())
		return output