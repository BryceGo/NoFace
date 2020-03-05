import cv2
import numpy as np
import time
import os
import copy
import sys
from math import ceil
from utils import videoManager
from ui import main_ui
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QWidget
from PyQt5.QtCore import QThread, QObject, pyqtSignal


# Helper functions
def openFile():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog

    dialog = QFileDialog()
    dialog.setNameFilters(["*.mp4", "*.avi"])
    dialog.exec()
    return dialog.selectedFiles()

def saveFile():
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    
    window = QtWidgets.QWidget()
    save = QFileDialog.getSaveFileName(window, 'Save File')
    if save != None and len(save) > 1:
        return save[0]
    else:
        return None


class VideoPlayer(QThread):

    def __init__(self, signal):
        super(VideoPlayer, self).__init__()
        self.vManager = videoManager.videoManager()
        self.filename = ''
        self.output_file = ''
        self.from_file = True
        self.save_file = True
        self.process = 'draw'
        self.signal = signal

    def run(self):

        self.vManager.stop_lock.acquire()
        self.stop = False
        self.vManager.stop_lock.release()

        self.vManager.process_video(filename=self.filename,
                                    output_file=self.output_file,
                                    from_file=self.from_file,
                                    save_file=self.save_file,
                                    process=self.process,
                                    signal=self.signal)

    def stop_manager(self):
        self.vManager.stop_video()

class MainWindow(QObject):

    vp_signal = pyqtSignal(int)
    def __init__(self):
        super(MainWindow, self).__init__()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.source_files = None
        self.destination_file = None
        self.vp_signal.connect(self.update_progressBar)
        self.video_player = VideoPlayer(self.vp_signal)

    def run(self):
        self.ui.b_browse.clicked.connect(self.browse_onclick)
        self.ui.b_saveAs.clicked.connect(self.saveAs_onclick)
        self.ui.b_liveStream.clicked.connect(self.liveStream_onclick)
        self.ui.b_analyzeVideo.clicked.connect(self.analyzeVideo_onclick)
        self.ui.b_stop.clicked.connect(self.stop_onclick)

        self.window.show()
        sys.exit(self.app.exec_())

    def browse_onclick(self):
        files = openFile()
        self.ui.t_source.setText("Source: {}".format(','.join(files)))
        self.source_files = files

        if len(files) > 0:
            self.ui.t_main.append("Set source file(s): {}".format(','.join(files)))
        return

    def saveAs_onclick(self):
        file = saveFile()
        self.ui.t_destination.setText("Destination: {}".format(file))
        self.destination_file = file

        if file != None:
            self.ui.t_main.append("Set destination file: {}".format(file))

        return

    def liveStream_onclick(self):
        self.video_player.from_file = False
        self.video_player.save_file = False

        if self.ui.r_drawFaces.isChecked():
            self.video_player.process = 'draw'
        elif self.ui.r_blurFaces.isChecked():
            self.video_player.process = 'blur'
        elif self.ui.r_pixelateFaces.isChecked():
            self.video_player.process = 'pixelate'

        self.video_player.start()
        self.ui.t_main.append("Live stream started...")

    def analyzeVideo_onclick(self):


        if isinstance(self.source_files, list) and len(self.source_files) != 0:
            self.video_player.from_file = True
            self.video_player.filename = self.source_files[0]
        else:
            self.video_player.from_file = False
            self.video_player.filename = None

        if self.destination_file != None:
            self.video_player.save_file = True
            self.video_player.output_file = self.destination_file
        else:
            self.video_player.save_file = False
            self.video_player.output_file = None


        if self.ui.r_drawFaces.isChecked():
            self.video_player.process = 'draw'
        elif self.ui.r_blurFaces.isChecked():
            self.video_player.process = 'blur'
        elif self.ui.r_pixelateFaces.isChecked():
            self.video_player.process = 'pixelate'

        self.video_player.start()
        self.ui.t_main.append("Started processing video...")

    def stop_onclick(self):
        self.video_player.stop_manager()
        self.ui.t_main.append("Stopped processing video...")

    def update_progressBar(self, value):
        self.ui.progressBar.setValue(value)
        if value == 100:
            self.ui.t_main.append("Completed processing video")


if __name__ == '__main__':
    main_ui = MainWindow()
    main_ui.run()

    # vm = videoManager.videoManager()
    # vm.start_video(filename="faces.mp4", save_file=False)
    # while True:
    #     pass
