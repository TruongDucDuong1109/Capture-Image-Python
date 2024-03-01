import sys
import cv2
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self._run_flag = True
        self.capture = cv2.VideoCapture(0)

    def run(self):
        while self._run_flag:
            ret, cv_img = self.capture.read()
            if ret:
                qt_img = self.convert_cv_qt(cv_img)
                self.change_pixmap_signal.emit(qt_img)

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
        self.SHOW.clicked.connect(self.start_video)
        self.TEXT.setText('Press "SHOW" to connect with camera')
        self.CAPTURE.clicked.connect(self.CaptureClicked)
        self.QUIT.clicked.connect(self.quitClicked)
        self.thread = None

    @pyqtSlot()
    def start_video(self):
        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()

    @pyqtSlot(QImage)
    def update_image(self, img):
        self.imgLabel.setPixmap(QPixmap.fromImage(img))

    def CaptureClicked(self):
        if self.thread is not None:
            frame = self.thread.capture.read()[1]
            if frame is not None:
                cv2.imwrite(f"image{self.value}.jpg", frame)
                self.TEXT.setText('Image captured')
                self.value += 1

    def quitClicked(self):
        if self.thread is not None:
            self.thread.stop()
        sys.exit()

app = QApplication(sys.argv)
window = TehseenCode()
window.show()
sys.exit(app.exec_())
