from utils import yoloDetector
import cv2
import numpy as np
from math import ceil
import time
import copy


class faceManager:

    def __init__(self, cascade_file = "./cascades/haarcascade_frontalface_default.xml"):
        self.cascade =  cv2.CascadeClassifier(cascade_file)
        self.error_flag = False
        self.yolo = yoloDetector.yolov3Manager()

    def detect_faces(self, image, threshold = 5):
        faces = self.cascade.detectMultiScale(image,1.3,threshold)
        return faces

    def detect_faces_yolo(self, image, confidence_threshold = 0.5, nonmax_threshold = 0.4):
        return self.yolo.process_image(image, confidence_threshold, nonmax_threshold)

    # def get_iou(self, coord1, coord2):
    #     # Coordinates have to be as a tuple of the form (x,y,w,h)
    #     # Taken from:
    #     # https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/ 
    #     xA = max(coord1[0], coord2[0])
    #     yA = max(coord1[1], coord2[1])
    #     xB = min(coord1[0]+coord1[2], coord2[0]+coord2[2])
    #     yB = min(coord1[0]+coord1[3], coord2[0]+coord2[3])

    #     intersection = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    #     box1_area = (coord1[2] + 1)*(coord1[3] + 1)
    #     box2_area = (coord2[2] + 1)*(coord2[3] + 1)

    #     return abs(float(intersection)/float(box1_area + box2_area - intersection))


    def track_faces(self, frame, detected_faces=[], faces_currently_tracking=[], iou_threshold = 0.3):
        # faces_currently_tracking = (tracker, bbox)

        if len(detected_faces) == 0 and len(faces_currently_tracking) == 0:
            return []

        current_trackers = []
        current_bbox = []

        height = frame.shape[0]
        width = frame.shape[1]

        for tracker, bound_box in faces_currently_tracking:
            success, bbox = tracker.update(frame)

            bbox = (max(0,int(bbox[0])), max(0,int(bbox[1])), max(0,int(bbox[2])), max(0,int(bbox[3])))

            if success and (bbox[0] < width or bbox[1] < height) and (bbox[2] != 0 and bbox[3] != 0):
                current_trackers.append(tracker)
                current_bbox.append(bbox)


        indices = cv2.dnn.NMSBoxes(current_bbox + detected_faces, 
                    [0.7 for i in range(0, len(current_bbox))] + [1.0 for i in range(0, len(detected_faces))],
                    0.5,
                    0.4)


        currently_tracking = []
        for i in indices:
            index = i[0]
            if index < len(current_bbox):
                currently_tracking.append((current_trackers[index], current_bbox[index]))

            else:
                box = tuple(detected_faces[index - len(current_bbox)])

                tracker = cv2.TrackerKCF_create()
                tracker.init(frame, box)

                if (box[0] < width or box[1] < height) and (box[2] != 0 and box[3] != 0):
                    currently_tracking.append((tracker, box))
        
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

    def draw_frame(self, frame, faces, color=(0,255,0)):
        y_max = frame.shape[0]
        x_max = frame.shape[1]

        for (tracker, (x,y,w,h)) in faces:

            if (x >= x_max or y >= y_max) or frame[y:y+h, x:x+w].shape[0] <= 3 or frame[y:y+h, x:x+w].shape[1] <= 3:
                continue
            
            frame = cv2.rectangle(frame, (x,y), (x+w,y+h), color, 1)
        return frame

    def pixelate_frame(self, frame, faces, division = 10):

        y_max = frame.shape[0]
        x_max = frame.shape[1]

        for (tracker, (x,y,w,h)) in faces:

            if (x >= x_max or y >= y_max) or frame[y:y+h, x:x+w].shape[0] <= 3 or frame[y:y+h, x:x+w].shape[1] <= 3:
                continue

            if len(frame.shape) > 2:
                cut_image = frame[y:y+h, x:x+w, :]
                
                rows, cols, dims = cut_image.shape
                for i in range(1, division+1):
                    for j in range(1, division+1):
                        for k in range(0,dims):
                            try:
                                cut_square = frame[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols), k]
                                avg = int(np.average(cut_square))
                                frame[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols), k].fill(avg)
                            except:
                                pass

            else:
                cut_image = frame[y:y+h, x:x+w]
                rows, cols = cut_image.shape

                for i in range(1, division+1):
                    for j in range(1, division+1):
                        try:
                            cut_square = frame[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols)]
                            avg = int(np.average(cut_square))
                            frame[y+int(((i-1)/division)*rows):y+int((i/division)*rows), x+int(((j-1)/division)*cols):x+int((j/division)*cols)].fill(avg)
                        except:
                            pass
        return frame

    def blur_frame(self, frame, faces, intensity = 5):

        y_max = frame.shape[0]
        x_max = frame.shape[1]

        for (tracker, (x,y,w,h)) in faces:
            shape = ceil(max(w,h)/intensity)
            if shape == 0:
                shape = 1
            kernel = np.ones((shape,shape), np.float32)/(shape*shape)

            # No point in blurring pixels if they are too small
            if (x >= x_max or y >= y_max) or frame[y:y+h, x:x+w].shape[0] <= 3 or frame[y:y+h, x:x+w].shape[1] <= 3:
                continue

            if len(frame.shape) > 2:
                for i in range(0,frame.shape[2]):
                    frame[y:y+h, x:x+w, i] = cv2.filter2D(frame[y:y+h, x:x+w, i], -1, kernel)
            else:
                frame[y:y+h, x:x+w] = cv2.filter2D(frame[y:y+h, x:x+w], -1, kernel)

            print((x,y,w,h), frame.shape)

        return frame

    def process_frame(self, frame, faces, type = 'draw'):
        if type == 'draw':
            return self.draw_frame(frame, faces)

        elif type == 'blur':
            return self.blur_frame(frame, faces)

        elif type == 'pixelate':
            return self.pixelate_frame(frame, faces)
        else:
            return frame
