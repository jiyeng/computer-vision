import cv2
import numpy as np
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt
import winsound

class TrafficWeak(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('교통약자 보호')
        self.setGeometry(200, 200, 700, 300)

        # UI Elements
        self.signButton = QPushButton('표지판 등록', self)
        self.signButton.setGeometry(10, 10, 100, 30)
        self.signButton.clicked.connect(self.signFunction)

        self.roadButton = QPushButton('도로 영상 불러옴', self)
        self.roadButton.setGeometry(120, 10, 150, 30)
        self.roadButton.clicked.connect(self.roadFunction)

        self.recognitionButton = QPushButton('인식', self)
        self.recognitionButton.setGeometry(280, 10, 100, 30)
        self.recognitionButton.clicked.connect(self.recognitionFunction)

        self.quitButton = QPushButton('나가기', self)
        self.quitButton.setGeometry(390, 10, 100, 30)
        self.quitButton.clicked.connect(self.quitFunction)

        self.label = QLabel('환영합니다!', self)
        self.label.setGeometry(10, 50, 600, 30)

        # Variables
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.signFiles = [
            os.path.join(base_dir, 'child.png'), 
            os.path.join(base_dir, 'elder.png'), 
            os.path.join(base_dir, 'disabled.png')
        ]  # 표지판 이미지 파일 경로
        self.signLabels = ['어린이 보호구역', '노인 보호구역', '장애인 보호구역']
        self.signImgs = []
        self.roadImg = None

    def signFunction(self):
        self.label.setText('교통약자 표지판을 등록합니다.')
        self.signImgs = []
        for fname in self.signFiles:
            img = cv2.imread(fname)
            if img is not None:
                self.signImgs.append(img)
                cv2.imshow(fname, img)
        if not self.signImgs:
            self.label.setText('표지판 이미지를 불러올 수 없습니다.')

    def roadFunction(self):
        if not self.signImgs:
            self.label.setText('먼저 표지판을 등록하세요.')
            return

        fname, _ = QFileDialog.getOpenFileName(self, '도로 영상 선택', '', 'Image Files (*.png *.jpg *.jpeg *.bmp)')
        if fname:
            self.roadImg = cv2.imread(fname)
            if self.roadImg is not None:
                cv2.imshow('Road Scene', self.roadImg)
                self.label.setText('도로 영상을 불러왔습니다.')
            else:
                self.label.setText('도로 영상을 불러올 수 없습니다.')

    def recognitionFunction(self):
        if self.roadImg is None:
            self.label.setText('먼저 도로 영상을 입력하세요.')
            return

        if not self.signImgs:
            self.label.setText('먼저 표지판을 등록하세요.')
            return

        sift = cv2.SIFT_create()

        # 등록된 표지판 키포인트와 기술자 추출
        signDescriptors = []
        for img in self.signImgs:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            kp, des = sift.detectAndCompute(gray, None)
            signDescriptors.append((kp, des))

        # 도로 영상 키포인트와 기술자 추출
        grayRoad = cv2.cvtColor(self.roadImg, cv2.COLOR_BGR2GRAY)
        roadKp, roadDes = sift.detectAndCompute(grayRoad, None)

        matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        bestMatchIdx = -1
        maxGoodMatches = 0
        bestGoodMatches = []

        # 매칭 비교
        for idx, (kp, des) in enumerate(signDescriptors):
            matches = matcher.knnMatch(des, roadDes, k=2)
            goodMatches = []
            for m, n in matches:
                if m.distance < 0.7 * n.distance:
                    goodMatches.append(m)

            if len(goodMatches) > maxGoodMatches:
                maxGoodMatches = len(goodMatches)
                bestMatchIdx = idx
                bestGoodMatches = goodMatches

        # 결과 시각화
        if maxGoodMatches > 10:  # 매칭 조건: 10개 이상의 좋은 매칭
            self.label.setText(f'{self.signLabels[bestMatchIdx]}입니다. 주의하세요!')
            winsound.Beep(3000, 500)

            # 호모그래피 계산
            srcPoints = np.float32([signDescriptors[bestMatchIdx][0][m.queryIdx].pt for m in bestGoodMatches]).reshape(-1, 1, 2)
            dstPoints = np.float32([roadKp[m.trainIdx].pt for m in bestGoodMatches]).reshape(-1, 1, 2)
            H, _ = cv2.findHomography(srcPoints, dstPoints, cv2.RANSAC, 5.0)

            # 등록된 표지판 크기 가져오기
            h, w = self.signImgs[bestMatchIdx].shape[:2]
            pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2)

            # 도로 영상에 투영
            dst = cv2.perspectiveTransform(pts, H)
            cv2.polylines(self.roadImg, [np.int32(dst)], True, (0, 255, 0), 3)

            # 매칭된 특징점 시각화
            imgMatch = cv2.drawMatches(self.signImgs[bestMatchIdx], signDescriptors[bestMatchIdx][0],
                                       self.roadImg, roadKp, bestGoodMatches, None,
                                       flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            cv2.imshow("Matches and Homography", imgMatch)
        else:
            self.label.setText('표지판이 인식되지 않았습니다.')

    def quitFunction(self):
        cv2.destroyAllWindows()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TrafficWeak()
    win.show()
    sys.exit(app.exec())
