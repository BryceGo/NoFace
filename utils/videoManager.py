import threading
import cv2
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
		self.fm = faceManager()
		self.status_queue = queue.Queue()
		self.stop_lock = threading.Lock()
		self.stop = False
		self.tracked_thread = None

	def stop_video(self):
		self.stop_lock.acquire()
		self.stop = True
		self.stop_lock.release()
		self.tracked_thread = None

	def start_video(self, filename, output_file, from_file = True, save_file=True, model='yl'):

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

	def process_video(self, filename, output_file, from_file = True, save_file=True, model='yl'):

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

		if save_file == True:
        	video_writer = cv2.VideoWriter(output_file, cv2.VideoWriter_fourcc('M','J','P','G'), fps, (width, height))
        else:
        	video_writer = _videoShow()

        count = 0
        total_count = 1
        current_faces = []

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


			if count % 5 == 0:
				count = 0

				# Place video detection here
				pass
			else:
				# Place video object detection here
				pass


			total_count += 1
			count += 1

		cap.release()
		video_writer.release()
		cv2.destroyAllWindows()
