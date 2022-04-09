from cProfile import label
from time import sleep
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
sys.path.append(r"E:/gh_luck/taurus/航天智能车/socket_ui") 
from socketclient import socket_client
from threading import Thread,Lock

from ui_string import ui_String
from ui_centre import ui_Centre
from ui_plot import ui_Plot
from ui_setting import ui_Setting
from ui_camera import ui_Camera
from ui_help import ui_Help

#from ui.ui_menu import Ui_MainWindow
from ui import qt_source_qr

class ui_Menu():

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = uic.loadUi("ui/ui_menu.ui")
        #self.ui.setWindowOpacity(0.9) #设置背景透明度 0为完全透明
        #self.ui.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.ui.setWindowTitle("中央任务调度系统主页")
        self.ui.setWindowIcon(QIcon("logo.ico"))
        

        self.ui.pushButton_1.clicked.connect(self.Button_1)
        self.ui.pushButton_2.clicked.connect(self.Button_2)
        self.ui.pushButton_3.clicked.connect(self.Button_3)
        self.ui.pushButton_4.clicked.connect(self.Button_4)
        self.ui.pushButton_5.clicked.connect(self.Button_5)
        self.ui.pushButton_6.clicked.connect(self.Button_6)

        self.ui.pushButton_close_ui.clicked.connect(self.back)
        self.ui.pushButton_share.clicked.connect(self.show_message)



    #中央控制系统
    def Button_1(self):
        #app = QApplication([])
        stats = ui_Centre()
        stats.ui.show()
        #self.ui.close()
        #app.exec_()   
    #系统监控
    def Button_2(self):
        stats = ui_Plot()
        stats.ui.show()
        #self.ui.close()
        app.exec_() 
    #串口调试
    def Button_3(self):
        stats = ui_String()
        stats.ui.show()
        #self.ui.close()
        app.exec_()  
    #遥控器
    def Button_4(self):
        stats = ui_Camera()
        stats.ui.show()
        #self.ui.close()
        app.exec_() 
    #系统与设置
    def Button_5(self):
        stats = ui_Setting()
        stats.ui.show()
        #self.ui.close()
        app.exec_() 
    #帮助
    def Button_6(self):
        stats = ui_Help()
        stats.ui.show()
        #self.ui.close()
        app.exec_() 

    #帮助
    def back(self):
        self.ui.close()

    def show_message(self):
        QMessageBox.information(self.ui, "提示", "该功能正在努力开发中，敬请期待...",
                                QMessageBox.Yes)

    



if __name__ == '__main__':

    app = QApplication([])
    stats = ui_Menu()
    stats.ui.show()
    app.exec_()     