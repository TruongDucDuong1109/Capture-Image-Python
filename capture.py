import sys

import cv2

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class tehseencode (QDialog):
    def __init__(self):
        super(tehseencode,self).init__()

        loadUi('tehseencode.ui',self)
        self.logic = 0
        self.value = 1
        self.SHOW.clicked.connect(self.onClicked)
        self.TEXT.setText('Press "SHOW" to connect with camera')
        self.CAPTURE.clicked.connect(self.CaptureClicked)

    @pyqtSlot()
    def onClicked (self):
        self.TEXT.setText('Connecting to camera')
        cap = cv2.VideoCapture(1)
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret == True:
                self.displayImage(frame, 1)
                cv2.waitKey()

                if(self.logic == 2):
                    self.value = self.value + 1
                    cv2.imwrite('image'+str(self.value)+'.jpg',frame)

                    self.logic = 1
                    self.TEXT.setText('Image captured')
            else:
                print('No image captured')
            
            cap.release()
            cv2.destroyAllWindows()

    def CaptureClicked(self):
        self.logic = 2
    
    def displayImage(self,img,window=1):
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img, img.shape[1], img.shape[0], qformat)
        img = img.rgbSwapped()
        self.imglabel.setPixmap(QPixmap.fromImage(img))
        self.imglabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

app = QApplication(sys.argv)
window = tehseencode()
window.show()
try:
    sys.exit(app.exec_())
except:
    print('Exiting')