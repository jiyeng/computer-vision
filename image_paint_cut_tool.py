import cv2
import numpy as np
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

class Orim(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('오림')
        self.setGeometry(200, 200, 800, 600)

        # Buttons
        self.fileButton = QPushButton('파일', self)
        self.fileButton.setGeometry(10, 10, 100, 30)
        self.fileButton.clicked.connect(self.fileOpenFunction)

        self.paintButton = QPushButton('페인팅', self)
        self.paintButton.setGeometry(120, 10, 100, 30)
        self.paintButton.clicked.connect(self.paintFunction)
        self.paintButton.setEnabled(False)

        self.cutButton = QPushButton('오림', self)
        self.cutButton.setGeometry(230, 10, 100, 30)
        self.cutButton.clicked.connect(self.cutFunction)
        self.cutButton.setEnabled(False)

        self.incButton = QPushButton('+', self)
        self.incButton.setGeometry(340, 10, 50, 30)
        self.incButton.clicked.connect(self.incFunction)

        self.decButton = QPushButton('-', self)
        self.decButton.setGeometry(400, 10, 50, 30)
        self.decButton.clicked.connect(self.decFunction)

        self.saveButton = QPushButton('저장', self)
        self.saveButton.setGeometry(460, 10, 100, 30)
        self.saveButton.clicked.connect(self.saveFunction)
        self.saveButton.setEnabled(False)

        self.quitButton = QPushButton('나가기', self)
        self.quitButton.setGeometry(570, 10, 100, 30)
        self.quitButton.clicked.connect(self.quitFunction)

        # Image Display
        self.imageLabel = QLabel(self)
        self.imageLabel.setGeometry(10, 50, 780, 540)
        self.imageLabel.setStyleSheet("border: 1px solid black;")

        # Variables
        self.img = None
        self.img_show = None
        self.mask = None
        self.BrushSize = 5
        self.LColor, self.RColor = (0, 0, 255), (255, 0, 0)  # Foreground: Blue, Background: Red

    def fileOpenFunction(self):
        fname, _ = QFileDialog.getOpenFileName(self, '파일 열기', './', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fname:
            self.img = cv2.imread(fname)
            self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
            self.img_show = self.img.copy()
            self.mask = np.zeros(self.img.shape[:2], dtype=np.uint8)
            self.mask[:, :] = cv2.GC_PR_BGD  # Initialize as probable background
            self.updateImage()
            self.paintButton.setEnabled(True)
            self.cutButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def updateImage(self):
        if self.img_show is not None:
            h, w, ch = self.img_show.shape
            bytes_per_line = ch * w
            qimg = QImage(self.img_show.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg).scaled(self.imageLabel.width(), self.imageLabel.height(), Qt.AspectRatioMode.KeepAspectRatio)
            self.imageLabel.setPixmap(pixmap)

    def paintFunction(self):
        self.paintingActive = True
        self.imageLabel.mousePressEvent = self.startPainting
        self.imageLabel.mouseMoveEvent = self.paint
        self.imageLabel.mouseReleaseEvent = self.stopPainting

    def startPainting(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.paintingType = 'foreground'
        elif event.button() == Qt.MouseButton.RightButton:
            self.paintingType = 'background'

    def paint(self, event):
        if self.paintingActive and self.img_show is not None:
            label_width = self.imageLabel.width()
            label_height = self.imageLabel.height()
            img_width = self.img.shape[1]
            img_height = self.img.shape[0]

            # Calculate scaling and offset
            scale = min(label_width / img_width, label_height / img_height)
            scaled_width = img_width * scale
            scaled_height = img_height * scale
            offset_x = (label_width - scaled_width) / 2
            offset_y = (label_height - scaled_height) / 2

            # Adjust mouse position relative to QLabel
            x = int((event.pos().x() - offset_x) / scale)
            y = int((event.pos().y() - offset_y) / scale)

            # Ensure coordinates are within bounds
            x = max(0, min(self.img.shape[1] - 1, x))
            y = max(0, min(self.img.shape[0] - 1, y))

            # Draw on the image
            if self.paintingType == 'foreground':
                cv2.circle(self.img_show, (x, y), self.BrushSize, self.LColor, -1)
                cv2.circle(self.mask, (x, y), self.BrushSize, cv2.GC_FGD, -1)
            elif self.paintingType == 'background':
                cv2.circle(self.img_show, (x, y), self.BrushSize, self.RColor, -1)
                cv2.circle(self.mask, (x, y), self.BrushSize, cv2.GC_BGD, -1)

            self.updateImage()

    def stopPainting(self, event):
        self.paintingActive = False

    def cutFunction(self):
        background = np.zeros((1, 65), np.float64)
        foreground = np.zeros((1, 65), np.float64)
        cv2.grabCut(self.img, self.mask, None, background, foreground, 5, cv2.GC_INIT_WITH_MASK)
        mask2 = np.where((self.mask == cv2.GC_FGD) | (self.mask == cv2.GC_PR_FGD), 1, 0).astype('uint8')
        self.img_show = self.img * mask2[:, :, np.newaxis]
        self.updateImage()

    def incFunction(self):
        self.BrushSize = min(50, self.BrushSize + 1)

    def decFunction(self):
        self.BrushSize = max(1, self.BrushSize - 1)

    def saveFunction(self):
        fname, _ = QFileDialog.getSaveFileName(self, '이미지 저장', './', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fname:
            cv2.imwrite(fname, cv2.cvtColor(self.img_show, cv2.COLOR_RGB2BGR))

    def quitFunction(self):
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Orim()
    win.show()
    sys.exit(app.exec())
