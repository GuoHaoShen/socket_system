from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from PyQt5.QtGui import *
sys.path.append(r"E:/gh_luck/taurus/航天智能车/socket_ui") 
from socketclient import socket_client
from threading import Thread,Lock
from time import sleep

class ui_String:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.sockclient=socket_client.SocketClient() 

        self.ui = uic.loadUi("ui/MainWindow_string.ui")
        self.ui.setWindowTitle("中央通信系统")
        self.ui.setWindowIcon(QIcon("logo.ico"))
        #处理三个按键
        self.ui.pushButton_sent.clicked.connect(self.send_edit)
        self.ui.pushButton_link.clicked.connect(self.link_server)
        self.ui.pushButton_close.clicked.connect(self.close_server)

        self.ui.pushButton_share.clicked.connect(self.show_message)

        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_close_ui.clicked.connect(self.back)

        self.ui.textBrowser.append("ui启动完成，请开始输入！")
        self.ui.textBrowser.document().setMaximumBlockCount(8)

        #创建新线程接收数据
        print("开启新线程接受数据")
        self.join_flag=0
        self.recv_thread = Thread(target=self.recv_data,daemon=True)
        self.recv_thread.start()

    def show_message(self):
        QMessageBox.information(self.ui, "提示", "该功能正在努力开发中，敬请期待...",
                                QMessageBox.Yes)

    #关闭线程并退出 
    def back(self):
        print("开始关闭线程")
        self.join_flag=1
        self.recv_thread.join()
        print("开始关闭ui")
        self.ui.close()

    #接收数据
    def recv_data(self):
        while self.join_flag==0:
            data = self.sockclient.recv_string()
            if data != "":
                print("从服务端受到数据：",data)
                self.ui.textBrowser.append("从服务端受到数据：%s"%data)
            sleep(0.01)


    #连接服务函数
    def link_server(self):
        print("点击连接服务器成功")
        #获取ip和prot
        IP=self.ui.lineEdit_ip.text()
        PORT=self.ui.lineEdit_prot.text()
        #开始连接
        print('开始连接')
        print("IP:",IP)
        print("PORT:",PORT)
        print(type(IP))
        print(type(PORT))
        self.sockclient.open_connect(IP,int(PORT))#开始连接
        print('连接成功')
        self.ui.textBrowser.append("连接成功！")

    def close_server(self):
        print("点击断开成功")
        self.sockclient.close_connect()
        print("断开连接")
        self.ui.textBrowser.append("断开连接！")

    def send_edit(self):
        print("点击发送成功")
        data=self.ui.lineEdit_input.text()
        self.sockclient.sent_string(data)
        self.ui.textBrowser.append("发送成功！")
        self.ui.textBrowser.append("发送数据为：%s"%data)

# if __name__ == '__main__':

#     app = QApplication([])
#     stats = ui_string()
#     stats.ui.show()
#     app.exec_()     