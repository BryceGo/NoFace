import cv2
import numpy as np
from math import ceil
import time
from utils.faceManager import faceManager
import os
from utils import yoloDetector as yd
import copy
from utils import videoManager

def main(file_name):
    ext = tuple([".3g2", ".3gp", ".asf", ".asx", ".avi", ".flv", \
            ".m2ts", ".mkv", ".mov", ".mp4", ".mpg", ".mpeg", \
            ".rm", ".swf", ".vob", ".wmv"])

    face_m = faceManager()

    if os.path.basename(file_name).endswith(ext) == True:
        cap = cv2.VideoCapture(file_name)
        
        if cap == None:
            return None
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        output_file = cv2.VideoWriter('test.avi', cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
        count = 0
        total_count = 0
        current_faces = []
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret == False:
                break

            total_count += 1
            print(total_count)

            o_image =  copy.deepcopy(frame)
            if count % 5 == 0:
                count = 0
                # detect_image = face_m.preprocess_image(frame)
                detect_image = frame
                faces = face_m.detect_faces_yolo(detect_image)

                current_faces = face_m.track_faces(frame = o_image, detected_faces = faces, faces_currently_tracking = current_faces)
                output_file.write(face_m.draw_frame(o_image, current_faces))

            else :
                current_faces = face_m.track_faces(frame = frame, faces_currently_tracking = current_faces)
                output_file.write(face_m.draw_frame(o_image, current_faces))

            count += 1
        
        cap.release()
        output_file.release()




if __name__ == '__main__':

    vm = videoManager.videoManager()
    vm.start_video(filename="faces.mp4", save_file=False)
    while True:
        pass

    # main("america.mp4")
