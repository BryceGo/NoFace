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

            self.input =  (
                    ffmpeg
                    .input(filename)
                    .output('pipe:', format='rawvideo', pix_fmt='rgb24')
                    .run_async(pipe_stdout=True, cmd=base_path + "ffmpeg")
                    )
            probe = ffmpeg.probe(filename, cmd=base_path + "ffprobe")
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            self.width = int(video_info['width'])
            self.height = int(video_info['height'])
            self.num_frames = int(video_info['nb_frames'])

            try:
                self.fps = int(Fraction(video_info['avg_frame_rate']))
            except:
                # Remove raised error
                raise Exception("ERROR--- fps")
                self.fps = 30
            self.dimensions = 3

        else:
            self.input = cv2.VideoCapture(0)
            self.width  = int(self.input.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.input.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.num_frames = 1
            self.fps = 30

        if save_file == True:
            self.output = (
                    ffmpeg
                    .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(self.width, self.height))
                    .output(output_file, pix_fmt='yuv420p')
                    .overwrite_output()
                    .run_async(pipe_stdin=True, cmd=base_path + "ffmpeg")
                    )
        else:
            # Nothing needed to construct
            pass

        self.input_file = filename
        self.output_file = output_file
        self.from_file = from_file
        self.save_file = save_file

        self.init_error = False
        if self.input == None:
            self.init_error = True


    def __del__(self):
        try:
            if self.from_file == True:
                self.input.stdout.close()
                self.input.wait()
            else:
                self.input.release()
        except Exception as e:
            raise e
            # TODO: DO nothing
            pass

        try:
            if self.save_file == True:
                self.output.stdin.close()
                self.output.wait()
        except Exception as e:
            raise e
            # TODO: DO nothing
            pass

        cv2.destroyAllWindows()

    def read(self):
        if self.from_file == True:
            in_bytes = self.input.stdout.read(self.width*self.height*self.dimensions)

            if not in_bytes:
                return False, np.array([], dtype=np.uint8)

            retVal = (
                np
                .frombuffer(in_bytes, np.uint8)
                .reshape([self.height, self.width, self.dimensions])
                )
            
            return True, retVal
        else:
            return self.input.read()

    def write(self, frame):
        print("Wrote frame, ---", frame.shape)
        if self.save_file == True:

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
