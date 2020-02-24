import cv2
import numpy as np
from math import ceil
import time
from utils.faceManager import faceManager
import os



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
        while (cap.isOpened()):
            ret, frame = cap.read()

            if ret == False:
                break

            output_file.write(face_m.pixelate(frame))
            count += 1
            if count %5 == 0:
                print(count)
        
        cap.release()
        output_file.release()




if __name__ == '__main__':

    # blurrer = faceManager()
    # blurred_image = blurrer.draw(cv2.imread(".\\images\\test.png"))
    # cv2.imshow('img', blurred_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # blurred_image = blurrer.blur(cv2.imread(".\\images\\test.png"))
    # cv2.imshow('img', blurred_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # blurred_image = blurrer.pixelate(cv2.imread(".\\images\\test.png"))
    # blurred_image = blurrer.pixelate(cv2.cvtColor(cv2.imread(".\\images\\test.png"), cv2.COLOR_BGR2GRAY))
    # cv2.imshow('img', blurred_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # main(".\\images\\test.png")

    main("faces.mp4")
