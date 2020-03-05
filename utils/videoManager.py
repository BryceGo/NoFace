import threading
import cv2
import os
import copy
import queue
from utils import faceManager
import threading

class _videoShow:
    def __init__(self):
        pass

    def __del__(self):
        pass

    def write(self, image):
        cv2.imshow('frame', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return False
        return True

    def release(self):
        self.__del__()

class videoManager:
    def __init__(self):
        self.fm = faceManager.faceManager()
        self.status_queue = queue.Queue()
        self.stop_lock = threading.Lock()
        self.stop = False
        self.tracked_thread = None

    def stop_video(self):
        self.stop_lock.acquire()
        self.stop = True
        self.stop_lock.release()
        self.tracked_thread = None

    def start_video(self, filename='', output_file='', from_file = True, save_file=True, model='yl'):

        if self.tracked_thread != None:
            if isinstance(self.tracked_thread, threading.Thread):
                if self.tracked_thread.is_alive():
                    return False
                else:
                    self.tracked_thread = None
            else:
                return False
        self.stop_lock.acquire()
        self.stop = False
        self.stop_lock.release()

        self.tracked_thread = threading.Thread(target = self.process_video, args = (filename, output_file, from_file, save_file, model))
        self.tracked_thread.start()
        return True

    def process_video(self, filename, output_file, from_file = True, save_file=True, model='yl', process = 'draw', signal=None):

        if from_file == True:
            if os.path.exists(filename) != True:
                raise Exception("Error, file not found!")
            cap = cv2.VideoCapture(filename)
        else:
            cap = cv2.VideoCapture(0)

        if cap == None:
            return None

        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if save_file == True:
            video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
        else:
            video_writer = _videoShow()

        count = 0
        total_count = 1
        current_faces = []

        if signal != None:
            signal.emit(0)
            
        while (cap.isOpened()):
            self.stop_lock.acquire()
            if self.stop == True:
                self.stop = False
                self.stop_lock.release()
                break
            self.stop_lock.release()

            ret, frame = cap.read()

            if ret == False:
                break

            original_image = copy.deepcopy(frame)

            if count % int(fps/3) == 0:
                count = 0

                if model == 'yl':
                    faces = self.fm.detect_faces_yolo(frame)

                    current_faces = self.fm.track_faces(frame = original_image, detected_faces = faces, faces_currently_tracking = current_faces)
                    video_writer.write(self.fm.process_frame(original_image, current_faces, process))

            else: #if count % 3 == 0:
                if model == 'yl':
                    current_faces = self.fm.track_faces(frame = original_image, faces_currently_tracking = current_faces)
                    video_writer.write(self.fm.process_frame(original_image, current_faces, process))
            # else:
            #     if model == 'yl':
            #         video_writer.write(self.fm.draw_frame(original_image, current_faces))

            if signal != None:
                if total_count % fps == 0:
                    signal.emit(int((float(total_count)/float(total_frames))*100))
                    # self.status_queue.put({"STATUS": "PROGRESS", "VALUE": int((float(total_count)/float(total_frames))*100)})

            total_count += 1
            count += 1
        if signal != None:
            signal.emit(100)
        # self.status_queue.put({"STATUS": "PROGRESS", "VALUE": 100})
        
        cap.release()
        video_writer.release()
        cv2.destroyAllWindows()