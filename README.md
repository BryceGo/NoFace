# No Face
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](./LICENSE)
*Place Gif Here*

# Introduction
No Face is an automated face blurring application, written in Python and capable of processing video files (MP4s and AVIs) and streams from video cameras. 

# Description
This project uses [OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html) and [Tiny YoloV3](https://pjreddie.com/darknet/yolo/) to perform face detection on target videos and camera live streams. [KCF Object Tracking](https://arxiv.org/pdf/1404.7584.pdf) was also used to periodically track faces accross the screen to reduce computational overhead.

The tiny yolov3 model was pre-trained on the COCO dataset and retrained on the WIDER face dataset: http://shuoyang1213.me/WIDERFACE/

All processing is done on CPU only

# Requirements
Operating Systems:
- Windows 10
- Ubuntu 18.04 (Currently being tested)

# Download and Run
### Windows 10:
- Download the zip [file]()
- Unzip the file
- Run the exe as admin
 
### Ubuntu 18.04:
- Download the tar [file]()
- Unzip the file
- Run ```./no_face```

# Usage
*Add Picture Here*
Click Browse to choose video file to process

*Add Picture Here*
Click the Save as button to name the save file

*Add Picture Here*
Click Analyze Video to process the video

Click the Stop button anytime to stop processing the video

*Add Picture here*
If a camera is connected and detected by your computer, you can also click the Live Stream button to process the video from the camera.

*Add Picture here*
Choose the option in the radio buttons to choose which type of processing to run

# Development Installation
### For Windows 10:

Download and install the latest release of [Python 3.6](https://www.python.org/downloads/)
Run the pip install
```
pip install -r requirements.txt
```

Download the yolov3-tiny model at (Insert link here)
Copy the yolov3-tiny weights and cfg into the current working directory.

Download the ffmpeg.exe from https://www.ffmpeg.org/download.html
Move ffmpeg.exe into the current directory

Run:
```
python noface.py
```

Build the executable by running:
```
windows_build.bat
```

---

### For Ubuntu 18.04:

**To be Continued**

---

# Notes
More information on how to train your own custom yolo weights can be found here:
https://pjreddie.com/darknet/yolo/
https://github.com/AlexeyAB/darknet