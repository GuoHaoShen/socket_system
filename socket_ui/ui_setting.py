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

class ui_Setting():

    def __init__(self):
        #初始化颜色空间
        self.typeface = 'Arial'
        self.text_size = 15
        self.thick_size = 10
        self.thick = False #粗体
        self.italics = False #斜体
        self.dele = False #删除线
        self.decline = False #下滑线

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("ui/ui_setting.ui")
        self.ui.setWindowTitle("系统与设置")
        self.ui.setWindowIcon(QIcon("logo.ico"))
        #返回键
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_close_ui.clicked.connect(self.back)

        self.ui.lineEdit_text.textChanged.connect(self.text_change)
        self.ui.lineEdit_text.setPlaceholderText('请在这里输入测试文本')

        self.ui.comboBox.currentIndexChanged.connect(self.typespace_change)
        self.ui.horizontalSlider_size.valueChanged.connect(self.size_change)
        self.ui.horizontalSlider_thick.valueChanged.connect(self.thick_size_change)

        self.ui.checkBox_thick.stateChanged.connect(self.checkbox_change)
        self.ui.checkBox_italics.stateChanged.connect(self.checkbox_change)
        self.ui.checkBox_dele.stateChanged.connect(self.checkbox_change)
        self.ui.checkBox_decline.stateChanged.connect(self.checkbox_change)
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
        
    #更新文本内容
    def update_text(self):
        font = QFont()   #实例化字体对象       
        font.setFamily(self.typeface)  #字体
        font.setBold(self.thick)  #加粗
        font.setItalic(self.italics)    #斜体
        font.setStrikeOut(self.dele)  #删除线
        font.setUnderline(self.decline)   #下划线
        font.setPointSize(self.text_size)   #字体大小
        font.setWeight(self.thick_size)   #可能是字体的粗细
        self.ui.label.setFont(font)


    def checkbox_change(self):
        if self.ui.checkBox_thick.isChecked():
            self.thick = True
        else:
            self.thick = False #粗体
        if self.ui.checkBox_italics.isChecked():
            self.italics = True
        else:
            self.italics = False #粗体
        if self.ui.checkBox_dele.isChecked():
            self.dele = True
        else:
            self.dele = False #粗体
        if self.ui.checkBox_decline.isChecked():
            self.decline = True
        else:
            self.decline = False #粗体
        self.update_text()

    #字体粗细改变
    def thick_size_change(self):
        self.thick_size = self.ui.horizontalSlider_thick.value()
        print('字体粗细变更为=%s'%self.thick_size)
        self.update_text()
    #字体大小改变
    def size_change(self):
        self.text_size = self.ui.horizontalSlider_size.value()
        print('字体大小变更为=%s'%self.text_size)
        self.update_text()
        #self.ui.label.setFont(QFont("Arial",size))
    #字体改变
    def typespace_change(self):
        print("字体变更为:",self.ui.comboBox.currentText())
        self.typeface =  self.ui.comboBox.currentText()
        self.update_text()
    #文字内容改变
    def text_change(self):
        text =  self.ui.lineEdit_text.text()
        self.ui.label.setText(text)
        

    def back(self):
            print("开始关闭ui")
            self.ui.close()
 