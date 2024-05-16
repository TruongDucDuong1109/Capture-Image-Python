import sys
import cv2
import os
from PyQt5 import QtCore
import numpy as np
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    frame_captured_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._run_flag = True
        # self.capture = cv2.VideoCapture('http://10.10.22.40:8080/video')
        self.capture = cv2.VideoCapture(1)
        
        self.current_frame = None

    def run(self):
        while self._run_flag:
            ret, cv_img = self.capture.read()
            if ret:
                
                qt_img = self.convert_cv_qt(cv_img)
                self.current_frame = qt_img
                self.change_pixmap_signal.emit(qt_img)
            else:
                print("Failed to receive frame from camera.")

    def stop(self):
        self._run_flag = False
        self.capture.release()
        self.quit()

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(640, 480, QtCore.Qt.KeepAspectRatio)
        return p

class TehseenCode(QDialog):
    def __init__(self):
        super(TehseenCode, self).__init__()
        loadUi('loadui.ui', self)
        self.logic = 0
        self.value = 1
        self.img_folder = "img"  
        os.makedirs(self.img_folder, exist_ok=True)
        self.SHOW.clicked.connect(self.start_video)
        self.TEXT.setText('Press "SHOW" to connect with camera')
        self.CAPTURE.clicked.connect(self.CaptureClicked)
        self.QUIT.clicked.connect(self.quitClicked)
        self.thread = None

    @pyqtSlot()
    def start_video(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.frame_captured_signal.connect(self.frameCaptured)
        self.thread.start()

    @pyqtSlot(QImage)
    def update_image(self, img):
        self.imgLabel.setPixmap(QPixmap.fromImage(img))

    @pyqtSlot()
    def frameCaptured(self):
        self.TEXT.setText('Image captured')

    def CaptureClicked(self):
        if self.thread is not None and self.thread.current_frame is not None:
            cv_img = self.convert_qt_cv(self.thread.current_frame)
            cv2.imwrite(f"img/image{self.value}.jpg", cv_img)
            self.value += 1
            self.thread.frame_captured_signal.emit()

    def convert_qt_cv(self, qt_img):
        qimage_to_cv = qt_img.convertToFormat(QImage.Format_RGB888)
        width = qimage_to_cv.width()
        height = qimage_to_cv.height()
        ptr = qimage_to_cv.constBits()
        ptr.setsize(qimage_to_cv.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)  
        return arr


    def quitClicked(self):
        if self.thread is not None:
            self.thread.stop()
        sys.exit()

app = QApplication(sys.argv)
window = TehseenCode()
window.show()
sys.exit(app.exec_())
