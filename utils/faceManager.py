import cv2
import numpy as np
from math import ceil
import time
import copy


class faceManager:

    def __init__(self, cascade_file = "./cascades/haarcascade_frontalface_default.xml"):
        self.cascade =  cv2.CascadeClassifier(cascade_file)
        self.error_flag = False

    def detect_faces(self, image, threshold = 5):
        faces = self.cascade.detectMultiScale(image,1.3,threshold)
        return faces

    def get_iou(self, coord1, coord2):
        # Coordinates have to be as a tuple of the form (x,y,w,h)
        # Taken from:
        # https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/ 
        xA = max(coord1[0], coord2[0])
        yA = max(coord1[1], coord2[1])
        xB = min(coord1[0]+coord1[2], coord2[0]+coord2[2])
        yB = min(coord1[0]+coord1[3], coord2[0]+coord2[3])

        intersection = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        box1_area = (coord1[2] + 1)*(coord1[3] + 1)
        box2_area = (coord2[2] + 1)*(coord2[3] + 1)

        return abs(float(intersection)/float(box1_area + box2_area - intersection))


    def track_faces(self, frame, detected_faces=[], faces_currently_tracking=[], iou_threshold = 0.6):
        # faces_currently_tracking = (tracker, bbox)

        currently_tracking = []

        for tracker, bound_box in faces_currently_tracking:
            success, bbox = tracker.update(frame)

            bbox = (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))

            if success:
                currently_tracking.append((tracker, bbox))

        for face in detected_faces:
            face = tuple(face)

            iou_pass = True

            for tracked in currently_tracking:
                if self.get_iou(face, tracked[1]) > iou_threshold:
                    iou_pass = False
                    break


            if iou_pass == True:
                # New face detected
                tracker = cv2.TrackerKCF_create()
                tracker.init(frame, face)

                currently_tracking.append((tracker, face))
        
        return currently_tracking


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

    def pixelate(self, image, division=10):
        original_image = copy.deepcopy(image)
        target_image = self.preprocess_image(image)

        faces = self.detect_faces(target_image)

        for (x,y,w,h) in faces:

            if len(original_image.shape) > 2:
                cut_image = original_image[y:y+h, x:x+w, :]
                
                rows, cols, dims = cut_image.shape

                for i in range(1, division+1):
                    for j in range(1, division+1):
                        for k in range(0,dims):
                            avg = int(np.average(original_image[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols), k]))
                            original_image[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols), k].fill(avg)

            else:
                cut_image = original_image[y:y+h, x:x+w]
                rows, cols = cut_image.shape

                for i in range(1, division+1):
                    for j in range(1, division+1):
                        avg = int(np.average(original_image[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols)]))
                        original_image[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols)].fill(avg)
        return original_image

    def draw(self, image, color=(0,255,0)):
        original_image = copy.deepcopy(image)
        target_image = self.preprocess_image(image)

        faces = self.detect_faces(target_image)

        for (x,y,w,h) in faces:
            original_image = cv2.rectangle(original_image, (x,y), (x+w,y+h), color, 1)
        return original_image

    def draw_frame(self, frame, faces, color=(0,255,0)):

        for (tracker, (x,y,w,h)) in faces:
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), color, 1)
        return frame