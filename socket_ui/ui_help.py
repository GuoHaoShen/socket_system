from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox,QLabel
import sys
from PyQt5.QtGui import *
from PyQt5.QtGui import QFont
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

class ui_Help():

    def __init__(self):
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("ui/ui_help.ui")
        self.ui.setWindowTitle("帮助")
        self.ui.setWindowIcon(QIcon("logo.ico"))
        #返回键
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
    
        
    def back(self):
            print("开始关闭ui")
            self.ui.close()
 