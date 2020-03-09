import threading
import cv2
import os
import copy
import queue
from utils import faceManager
from utils import fileManager
import threading
import ffmpeg
import sys

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

        try:
            base_path = sys._MEIPASS
        except:
            base_path = os.path.abspath(".")

        # Add temporary file

        file_manager = fileManager.fileManager(filename, output_file, from_file, save_file)

        if file_manager.init_error == True:
            return None

        width  = file_manager.width
        height = file_manager.height
        fps = file_manager.fps
        total_frames = file_manager.num_frames

        count = 0
        total_count = 1
        current_faces = []

        if signal != None:
            signal.emit(0)
            
        while (True):
            self.stop_lock.acquire()
            if self.stop == True:
                self.stop = False
                self.stop_lock.release()
                break
            self.stop_lock.release()

            ret, t_frame = file_manager.read()

            if ret == False:
                break

            frame = cv2.cvtColor(copy.deepcopy(t_frame), cv2.COLOR_RGB2BGR)

            original_image = copy.deepcopy(frame)

            if count % int(fps/5) == 0:
                count = 0

                if model == 'yl':
                    faces = self.fm.detect_faces_yolo(frame, confidence_threshold=0.3)

                    current_faces = self.fm.track_faces(frame = original_image, detected_faces = faces, faces_currently_tracking = current_faces)
                    file_manager.write(self.fm.process_frame(original_image, current_faces, process))

            else: #if count % 3 == 0:
                if model == 'yl':
                    current_faces = self.fm.track_faces(frame = original_image, faces_currently_tracking = current_faces)
                    file_manager.write(self.fm.process_frame(original_image, current_faces, process))

            if from_file == True and signal != None:
                if total_count % fps == 0:
                    signal.emit(int(min((float(total_count)/float(total_frames)), 1)*100))

            total_count += 1
            count += 1
        if signal != None:
            signal.emit(100)

        del file_manager