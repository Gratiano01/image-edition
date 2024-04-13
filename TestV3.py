import sys
from PyQt5 import QtGui, QtWidgets, QtCore, uic
import cv2
import numpy as np
import requests
from PyQt5.QtGui import QImage, QIcon, QPixmap

API_KEY = 'x2NyKaa6vYuArYwat4x0-NpIbM9CrwGU'
API_SECRET = 'OuHx-Xaey1QrORwdG7QetGG5JhOIC8g7'
MERGE_FACE_URL = 'https://api-us.faceplusplus.com/facepp/v1/mergeface'

def merge_faces(image_url, face_url, merge_url):
    payload = {
        'api_key': API_KEY,
        'api_secret': API_SECRET,
        'template_url': image_url,
        'merge_url': face_url
    }
    try:
        response = requests.post(MERGE_FACE_URL, data=payload)
        response_json = response.json()
        if 'result' in response_json:
            with open(merge_url, 'wb') as merge_file:
                merge_file.write(requests.get(response_json['result']).content)
            print("Merged face image saved successfully.")
        else:
            print("Failed to merge faces.")
    except requests.RequestException as e:
        print("Error occurred:", e)

form, base = uic.loadUiType("./image_edition_v3.ui")
print()
def OpenCvToQImage(cvMat):
    height, width = cvMat.shape[:2]
    bytesPerLine = 3 * width
    return QImage(cvMat.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()

class EditionWindow(base, form):
    def __init__(self):
        super(EditionWindow, self).__init__()
        self.setupUi(self)

        self.imageViewer = QtWidgets.QLabel(self)  # 使用 QLabel
        self.setCentralWidget(self.imageViewer)
        self.imageViewer.setGeometry(10, 10, 660, 440)  # 根据需要调整尺寸

        self.actionOpen.triggered.connect(self.open_image)
        self.actionSave.triggered.connect(self.save)
        self.actionSaveAs.triggered.connect(self.save_as)
        self.actionExit.triggered.connect(self.close)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)

        self.actionColorReplacement.triggered.connect(self.replace_color)
        self.actionTopography.triggered.connect(self.deform)
        self.actionFaceMerge.triggered.connect(self.merge_face)

        self.currentImage = None

    def open_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        print("filename",filename)
        if filename:
            self.currentImage = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
            print("currentImage=",self.currentImage)
            if self.currentImage is not None:
                print("图像加载成功。")
                self.display_image()
            else:
                print("无法加载图像，请检查图像文件和路径。")
                QtWidgets.QMessageBox.warning(self, "Error", "Could not load the image.")

    def display_image(self):
        if self.currentImage is not None:
            print("Image is loaded")  # 确认图像已加载
            cvMat = cv2.cvtColor(self.currentImage, cv2.COLOR_BGR2RGB)
            height, width, channel = cvMat.shape
            bytesPerLine = 3 * width
            qImg = QImage(cvMat.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.imageViewer.setPixmap(pixmap)
            self.imageViewer.adjustSize()
            print(self.currentImage)

        else:
            print("Failed to load the image")  # 图像加载失败

    def save(self):
        
        pass

    def save_as(self):

        pass

    def undo(self):

        pass

    def redo(self):

        pass

    def replace_color(self):

        pass

    def deform(self):

        pass

    def merge_face(self):

        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EditionWindow()
    window.show()
    sys.exit(app.exec_())
