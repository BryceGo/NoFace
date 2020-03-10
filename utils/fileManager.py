import cv2
import ffmpeg
import sys
import os
from fractions import Fraction
import numpy as np

class fileManager:

    def __init__(self, filename, output_file, from_file = True, save_file=True):
        try:
            base_path = sys._MEIPASS + "\\"
        except:
            base_path = os.path.abspath(".") + "\\"

        if from_file == True:
            if os.path.exists(filename) != True:
                raise Exception("Error, file not found!")

            self.input = cv2.VideoCapture(filename)
            self.width  = int(self.input.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.input.get(cv2.CAP_PROP_FRAME_HEIGHT)) 
            self.fps = int(self.input.get(cv2.CAP_PROP_FPS)) 
            self.num_frames = int(self.input.get(cv2.CAP_PROP_FRAME_COUNT))

        else:
            self.input = cv2.VideoCapture(0)
            self.width  = int(self.input.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.input.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.num_frames = 1
            self.fps = 30

        if save_file == True:
            self.output = (
                    ffmpeg
                    .input('pipe:', framerate=self.fps, format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(self.width, self.height))
                    .output(output_file, pix_fmt='yuv420p')
                    .overwrite_output()
                    .run_async(pipe_stdin=True, cmd=base_path + "ffmpeg")
                    )

        self.input_file = filename
        self.output_file = output_file
        self.from_file = from_file
        self.save_file = save_file

        self.init_error = False
        if self.input == None:
            self.init_error = True


    def __del__(self):
        try:
            self.input.release()
        except Exception as e:
            pass

        try:
            if self.save_file == True:
                self.output.stdin.close()
                self.output.wait()
        except Exception as e:
            pass

        cv2.destroyAllWindows()

    def read(self):
        return self.input.read()

    def write(self, frame):
        if self.save_file == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.output.stdin.write(
                frame
                .astype(np.uint8)
                .tobytes()
                )
            return True
        else:
            cv2.imshow('video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False
            return True
