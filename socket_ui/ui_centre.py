from pprint import pprint
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
sys.path.append(r"E:/gh_luck/taurus/航天智能车/socket_ui") 
from socketclient import socket_client
from threading import Thread,Lock
from time import sleep


class ui_Centre:

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit

        self.sockclient=socket_client.SocketClient() 
        self.ui = uic.loadUi("ui/ui_Centre.ui")
        self.ui.setWindowTitle("中央调度系统")
        self.ui.setWindowIcon(QIcon("logo.ico"))

        #设置按键
        self.ui.pushButton_link.clicked.connect(self.link_server)
        self.ui.pushButton_close.clicked.connect(self.close_server)
        self.ui.pushButton_send_v.clicked.connect(self.send_vel)
        self.ui.pushButton_reset_v.clicked.connect(self.reset_vel)
        self.ui.pushButton_send_p.clicked.connect(self.send_point)
        self.ui.pushButton_reset_p.clicked.connect(self.reset_point)

        self.ui.pushButton_share.clicked.connect(self.show_message)

        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_close_ui.clicked.connect(self.back)

        self.ui.textBrowser.append("ui启动完成，请开始输入！")
        self.ui.textBrowser.document().setMaximumBlockCount(8)

        self.vel_x = 0.3
        self.vel_y = 0.3
        self.vel_a = 0.3
        v_step_length = 0.1 
        a_step_length = 0.2

        self.ui.Button_leftfront.clicked.connect(lambda:self.control_vel(self.vel_x,0,self.vel_a))
        self.ui.Button_front.clicked.connect(lambda:self.control_vel(self.vel_x,0,0))
        self.ui.Button_rightfront.clicked.connect(lambda:self.control_vel(self.vel_x,0,-self.vel_a))
        self.ui.Button_left.clicked.connect(lambda:self.control_vel(0,self.vel_y,0))
        self.ui.Button_stop.clicked.connect(lambda:self.control_vel(0,0,0))
        self.ui.Button_right.clicked.connect(lambda:self.control_vel(0,-self.vel_y,0))
        self.ui.Button_leftback.clicked.connect(lambda:self.control_vel(-self.vel_x,0,self.vel_a))
        self.ui.Button_back.clicked.connect(lambda:self.control_vel(-self.vel_x,0,0))
        self.ui.Button_rightback.clicked.connect(lambda:self.control_vel(-self.vel_x,0,-self.vel_a))

        self.ui.Button_vx_up.clicked.connect(lambda:self.update_vel("vel_x",v_step_length))
        self.ui.Button_vx_down.clicked.connect(lambda:self.update_vel("vel_x",-v_step_length))
        self.ui.Button_vy_up.clicked.connect(lambda:self.update_vel("vel_y",v_step_length))
        self.ui.Button_vy_down.clicked.connect(lambda:self.update_vel("vel_y",-v_step_length))
        self.ui.Button_va_up.clicked.connect(lambda:self.update_vel("vel_a",a_step_length))
        self.ui.Button_va_down.clicked.connect(lambda:self.update_vel("vel_a",-a_step_length))
        

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
        print("开始关闭socket")
        self.sockclient.close_connect()
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
                #self.ui.textBrowser.append("从服务端受到数据：%s"%data)
            sleep(1)

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
        self.sockclient.open_connect(IP,int(PORT),if_recv=False)#开始连接，不需要接受消息
        print('连接成功')
        self.ui.textBrowser.append("连接成功！")
    #断开连接
    def close_server(self):
        print("点击断开成功")
        self.sockclient.close_connect()
        print("断开连接")
        self.ui.textBrowser.append("断开连接！")

    #遥控速度
    def control_vel(self,vx,vy,va):
        if self.ui.checkBox_ack.isChecked() and vy!=0:
            va = vy
        print("点击发送速度成功")
        self.ui.textBrowser.append("发送数据为：vx=%s vy=%s va=%s"%(vx,vy,va))
        try:
            self.sockclient.sent_vel(vx,vy,va)
        except:
            print("发送失败！")

    #更新控制速度
    def update_vel(self,v_type,change_data):
        if v_type == 'vel_x':
            self.vel_x += change_data
        elif v_type == 'vel_y':
            self.vel_y += change_data
        elif v_type == 'vel_a':
            self.vel_a += change_data
        self.ui.textBrowser_vel.append("遥控速度大小为：vx=%s vy=%s va=%s"%(self.vel_x,self.vel_y,self.vel_a))

    #发送速度
    def send_vel(self):
        print("点击发送速度成功")
        vx=self.ui.lineEdit_vx.text()
        vy=self.ui.lineEdit_vy.text()
        va=self.ui.lineEdit_va.text()
        self.sockclient.sent_vel(vx,vy,va)
        #self.ui.textBrowser.append("发送成功！")
        self.ui.textBrowser.append("发送数据为：vx=%s vy=%s va=%s"%(vx,vy,va))
    #发送坐标
    def send_point(self):
        print("点击发送速度成功")
        px=self.ui.lineEdit_px.text()
        py=self.ui.lineEdit_py.text()
        pa=self.ui.lineEdit_pa.text()
        self.sockclient.sent_point(px,py,pa)
        #self.ui.textBrowser.append("发送成功！")
        self.ui.textBrowser.append("发送数据为：px=%s py=%s pa=%s"%(px,py,pa))
    #清除框中速度
    def reset_vel(self):
        print("输入框清除成功！")
        self.ui.lineEdit_vx.setText("0")
        self.ui.lineEdit_vy.setText("0")
        self.ui.lineEdit_va.setText("0")

    #清除框中位置
    def reset_point(self):
        print("输入框清除成功！")
        self.ui.lineEdit_px.setText("0")
        self.ui.lineEdit_py.setText("0")
        self.ui.lineEdit_pa.setText("0")
    
