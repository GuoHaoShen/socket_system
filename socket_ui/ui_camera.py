from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from PyQt5.QtGui import *
import cv2
from PyQt5.QtCore import *
from numpy import empty
sys.path.append(r"E:/gh_luck/taurus/航天智能车/socket_ui") 
from socketclient import socket_client
from threading import Thread,Lock
from pyqtgraph.Qt import  QtCore
import pyqtgraph as pg
from time import sleep
import numpy as np

from ui import qt_source_qr

class ui_Camera():

    def __init__(self):
        #初始化颜色空间
        self.color_space = "RGB"
        self.bright = 1
        self.contrast = 10
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("ui/ui_camera.ui")

        self.ui.setWindowTitle("视觉调试助手")
        self.ui.setWindowIcon(QIcon("logo.ico"))
        #self.ui.setWindowOpacity(0.9) #设置背景透明度 0为完全透明
        #self.ui.setWindowFlags(Qt.WindowMinimizeButtonHint)

        self.timer_camera = QTimer() #初始化定时器
        self.cap = cv2.VideoCapture() #初始化摄像头
        self.CAM_NUM = 0

        #self.returnSignal = pyqtSignal()

        self.slot_init()
        
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_close_ui.clicked.connect(self.back)
        self.ui.pushButton_share.clicked.connect(self.show_message)

        #创建新线程接收数据
        print("开启新线程")
        self.join_flag=0
        self.recv_thread = Thread(target=self.recv_data,daemon=True)
        self.recv_thread.start()

    def show_message(self):
        QMessageBox.information(self.ui, "提示", "该功能正在努力开发中，敬请期待...",
                                QMessageBox.Yes)
    #接收数据
    def recv_data(self):
        while True:
            sleep(1)


    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
                #信号和槽连接
        #self.ui.pushButton_return.clicked.connect(self.returnSignal)
        self.ui.pushButton_open.clicked.connect(self.slotCameraButton)
        #设置刻度间距
        self.ui.horizontalSlider_bright.setSingleStep(0.2)
        self.ui.horizontalSlider_contrast.setSingleStep(0.2)
        #连接滑动条
        self.ui.horizontalSlider_bright.valueChanged.connect(self.bright_change)
        self.ui.horizontalSlider_contrast.valueChanged.connect(self.contrast_change)
        self.ui.comboBox.currentIndexChanged.connect(self.color_space_change)


    #显示摄像头数据
    def show_camera(self):
        #调整亮度和对比度   
        # alpha为对比度 a=1时是原图
        # beta为亮度，b=1时是原图，随着增加b (b>0)和减小b (b>0)，图像整体的灰度值上移或者下移
        def Contrast_and_Brightness(alpha, beta, img):
            blank = np.zeros(img.shape, img.dtype)
            # dst = alpha * img + beta * blank
            dst = cv2.addWeighted(img, alpha, blank, 1-alpha, beta)
            return dst

        flag,self.image = self.cap.read()
        show = cv2.resize(self.image,(800,700))
        
        #设置颜色空间
        if self.color_space == "RGB":
            show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        elif self.color_space == "HSV":
            show = cv2.cvtColor(show, cv2.COLOR_BGR2HSV)
        elif self.color_space == "GRAY":
            show = cv2.cvtColor(show, cv2.COLOR_BGR2GRAY)
            show = cv2.cvtColor(show, cv2.COLOR_GRAY2BGR)
            #show = show[:,:,0]        #第1通道
        #调整亮度和对比度 
        show = Contrast_and_Brightness(self.contrast*0.1,self.bright,show)
        showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        # if self.color_space != "GRAY":
        #     showImage = QImage(show.data, show.shape[1],show.shape[0],QImage.Format_RGB888)
        # else :
        #     showImage = QImage(show.data, show.shape[1], show.shape[0],QImage.Format_Grayscale16)
        self.ui.label_camera.setPixmap(QPixmap.fromImage(showImage))

    #打开关闭摄像头控制
    def slotCameraButton(self):
        print("按返回键成功")
        if self.timer_camera.isActive() == False:
            #打开摄像头并显示图像信息
            self.openCamera()
        else:
            #关闭摄像头并清空显示信息
            self.closeCamera()

    #打开摄像头
    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            msg = QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
            buttons=QMessageBox.Ok,
            defaultButton=QMessageBox.Ok)
        else:
            self.timer_camera.start(30)
            self.ui.pushButton_open.setText('关闭摄像头')

        #关闭摄像头
    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.ui.label_camera.clear()
        self.ui.pushButton_open.setText('打开摄像头')

    def back(self):
        print("开始关闭ui")
        self.ui.close()

    def bright_change(self):
        self.bright = self.ui.horizontalSlider_bright.value()
        print('亮度值变更为=%s'%self.bright)

    def contrast_change(self):
        self.contrast = self.ui.horizontalSlider_contrast.value()
        print('对比度值变更为=%s'%self.contrast)

    def color_space_change(self):
        self.color_space = self.ui.comboBox.currentText()
        print('颜色空间变更为=%s'%self.color_space)
    
  