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


def main(file_name):
    ext = tuple([".avi", ".mp4"])

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

class MainWindow():

    def __init__(self):
        # super(MainWindow, self).__init__()

        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QMainWindow()
        self.ui = main_ui.Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.vManager = videoManager.videoManager()
        self.source_files = None
        self.destination_file = None

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
        pass

    def analyzeVideo_onclick(self):
        pass

    def stop_onclick(self):
        pass



if __name__ == '__main__':
    main_ui = MainWindow()
    main_ui.run()

    # vm = videoManager.videoManager()
    # vm.start_video(filename="faces.mp4", save_file=False)
    # while True:
    #     pass
