from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMessageBox
import sys
from PyQt5.QtGui import *
from numpy import empty
sys.path.append(r"E:/gh_luck/taurus/航天智能车/socket_ui") 
from socketclient import socket_client
from threading import Thread,Lock
from pyqtgraph.Qt import  QtCore
import pyqtgraph as pg
from time import sleep

class ui_Plot():

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.sockclient=socket_client.SocketClient() 
        self.ui = uic.loadUi("ui/ui_plot.ui")
        self.ui.setWindowTitle("中央监控系统")
        self.ui.setWindowIcon(QIcon("logo.ico"))

        #设置按键
        self.ui.pushButton_link.clicked.connect(self.link_server)
        self.ui.pushButton_close.clicked.connect(self.close_server)

        self.ui.pushButton_share.clicked.connect(self.show_message)

        self.ui.textBrowser.append("ui启动完成，请开始输入！")

        self.start_plot()   #初始化图表
        print("初始化图表成功")
        self.ui.pushButton_back.clicked.connect(self.back)
        self.ui.pushButton_close_ui.clicked.connect(self.back)

        #创建新线程接收数据
        print("开启新线程接受数据")
        self.join_flag=0
        self.recv_thread = Thread(target=self.recv_data,daemon=True)
        self.recv_thread.start()
        
    def show_message(self):
        QMessageBox.information(self.ui, "提示", "该功能正在努力开发中，敬请期待...",
                                QMessageBox.Yes)
                                
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
        self.sockclient.open_connect(IP,int(PORT))#开始连接
        print('连接成功')
        self.ui.textBrowser.append("连接成功！")

    def close_server(self):
        print("点击断开成功")
        self.sockclient.close_connect()
        print("断开连接")
        self.ui.textBrowser.append("断开连接！")

        
    #初始化图表
    def start_plot(self):
        # 设置图表标题
        self.ui.plotwidget.setTitle("速度趋势图",
                         color='008080',
                         size='12pt')
        # 设置上下左右的label
        self.ui.plotwidget.setLabel("left","速度")
        self.ui.plotwidget.setLabel("bottom","时间")
        # 显示表格线
        self.ui.plotwidget.showGrid(x=True, y=True)
        # 背景色改为白色
        self.ui.plotwidget.setBackground('w')

        # 实时显示应该获取 PlotDataItem对象, 调用其setData方法，
        # 这样只重新plot该曲线，性能更高
        self.line_cvx = self.ui.plotwidget.plot(
            pen=pg.mkPen('#F2481B', width=2))
        self.line_cvy = self.ui.plotwidget.plot(
            pen=pg.mkPen('#BE7E4A', width=2))
        self.line_cva = self.ui.plotwidget.plot(
            pen=pg.mkPen('#4B2E2B', width=2))
        self.line_ovx = self.ui.plotwidget.plot(
            pen=pg.mkPen('#1661AB', width=2))
        self.line_ovy = self.ui.plotwidget.plot(
            pen=pg.mkPen('#12A182', width=2))
        self.line_ova = self.ui.plotwidget.plot(
            pen=pg.mkPen('#617172', width=2))

        self.i = 0
        self.x = [] # x轴的值
        self.y = [] # y轴的值

        #初始化数据数组
        self.vcx = []
        self.vcy = []
        self.vca = []
        self.ocx = []
        self.ocy = []
        self.oca = []

        self.stamp = [] #初始化横坐标 时间

        self.MAX_X = 10 #设置最大范围
        self.updata_time = 0.15

        # 启动定时器，每隔1秒通知刷新一次数据
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateData)
        self.timer.start(self.updata_time*1000)

    def updateData(self):

        def update_list(data,new_data,list_max):
            data.append(new_data)
            #print(len(data))
            if len(data)>list_max:
                #print("删除第一个元素")
                del(data[0])
            return data

        cvx_new,cvy_new,cva_new = self.sockclient.recv_cmdvel()
        ovx_new,ovy_new,ova_new = self.sockclient.recv_odom()
        #print("cvx_new",cvx_new)


        self.vcx = update_list(self.vcx,cvx_new,self.MAX_X)
        self.vcy = update_list(self.vcy,cvy_new,self.MAX_X)
        self.vca = update_list(self.vca,cva_new,self.MAX_X)
        self.ocx = update_list(self.ocx,ovx_new,self.MAX_X)
        self.ocy = update_list(self.ocy,ovy_new,self.MAX_X)
        self.oca = update_list(self.oca,ova_new,self.MAX_X)

        #计算最新时间并更新
        if len(self.stamp)!=0:
            new_time = self.stamp[len(self.stamp)-1] + self.updata_time 
        else:
            new_time = 0
        self.stamp = update_list(self.stamp,new_time,self.MAX_X)
        #print(self.stamp)
        empty_data=[]

        #更新图表
        if self.ui.checkBox_cvx.isChecked():
            self.line_cvx.setData(self.stamp,self.vcx)
        else: 
            self.line_cvx.setData(empty_data,empty_data)
        if self.ui.checkBox_cvy.isChecked():
            self.line_cvy.setData(self.stamp,self.vcy)
        else: 
            self.line_cvy.setData(empty_data,empty_data)
        if self.ui.checkBox_cva.isChecked():
            self.line_cva.setData(self.stamp,self.vca)
        else: 
            self.line_cva.setData(empty_data,empty_data)
        if self.ui.checkBox_ovx.isChecked():
            self.line_ovx.setData(self.stamp,self.ocx)
        else: 
            self.line_ovx.setData(empty_data,empty_data)    
        if self.ui.checkBox_ovy.isChecked():
            self.line_ovy.setData(self.stamp,self.ocy)
        else: 
            self.line_ovy.setData(empty_data,empty_data)    
        if self.ui.checkBox_ova.isChecked():
            self.line_ova.setData(self.stamp,self.oca)
        else: 
            self.line_ova.setData(empty_data,empty_data)    

        #更新状态显示端文本
        self.ui.textBrowser.clear()
        self.ui.textBrowser.append("小车状态数据为：")
        self.ui.textBrowser.append("发送端线速度-x为：%s"%cvx_new)
        self.ui.textBrowser.append("发送端线速度-y为：%s"%cvy_new)
        self.ui.textBrowser.append("发送端角速度-z为：%s"%cva_new)
        self.ui.textBrowser.append("里程计线速度-x为：%s"%ovx_new)
        self.ui.textBrowser.append("里程计线速度-y为：%s"%ovy_new)
        self.ui.textBrowser.append("里程计角速度-z为：%s"%ova_new)



# if __name__ == '__main__':

#     app = QApplication([])
#     stats = ui_Plot()
#     stats.ui.show()
#     app.exec_()     