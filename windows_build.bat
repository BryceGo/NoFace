pyinstaller --onefile -w --add-data "yolov3-tiny.cfg;." --add-data "yolov3-tiny.weights;." --hidden-import "pkg_resources.py2_warn" noface.py
pause