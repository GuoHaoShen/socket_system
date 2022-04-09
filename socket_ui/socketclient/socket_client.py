from ast import Pass
from socket import *
import json
from threading import Thread,Lock
from time import sleep

class SocketClient():
    def __init__(self):
        self.dataLock = Lock()
        self.odom_data={}
        self.imu_data={}
        self.string_data={}
        self.cmdvel_data={}
        self.read_json() 
        #self.open_connect(IP,PORT)   


    #开启连接
    def open_connect(self,IP,PORT,if_recv=True):
        # 实例化一个socket对象，指明协议
        self.dataSocket = socket(AF_INET, SOCK_STREAM)
        # 连接服务端socket
        self.dataSocket.connect((IP, PORT))
        #创建新线程接收数据
        if if_recv==True:
            self.join_flag=0
            self.recv_thread = Thread(target=self.recv_all,daemon=True)
            self.recv_thread.start()
    #关闭连接
    def close_connect(self):
        try:
            self.dataSocket.close()
            self.join_flag=1
            self.recv_thread.join()
        except:
            pass


    #读取json文件
    def read_json(self):
        with open("config/wtopic.json",'r') as load_f:
            self.wtopic = json.load(load_f)
            print("成功读取数据类型")
        self.topic_list = [] #话题名列表
        #导入话题名列表
        # 操作共享数据前，申请获取锁
        self.dataLock.acquire()
        for i in range(len(self.wtopic)):
            self.topic_list.append(self.wtopic[i]["topic_name"])
            if self.wtopic[i]["topic_name"]=="socket_string":
                self.string_data=self.wtopic[i]
                #print("string_data:",self.string_data)
            elif self.wtopic[i]["topic_name"]=="cmd_vel":
                self.cmdvel_data=self.wtopic[i]
            elif self.wtopic[i]["topic_name"]=="odom":
                self.odom_data=self.wtopic[i]
            elif self.wtopic[i]["topic_name"]=="imu":
                self.imu_data=self.wtopic[i]
        self.dataLock.release()

    def recv_all(self):
        while self.join_flag==0:
            recv_alldata = self.dataSocket.recv(1024)
            print("收到数据为：",recv_alldata)
            #print("数据类型为：",type(recv_alldata))
            try:
                recv_alldata = json.loads(recv_alldata.decode())
                print("数据类型为：",type(recv_alldata))
                print("recv_alldata : ",recv_alldata)
                # for i in range(len(recv_alldata)):
                #     print("recv_alldata[i][topic_name] : ",recv_alldata[i][0])
                #     print("recv_alldata[i] : ",recv_alldata[i])
                if recv_alldata["topic_name"] in self.topic_list:
                    topic_name=recv_alldata["topic_name"]

                    # 操作共享数据前，申请获取锁
                    self.dataLock.acquire()
                    if topic_name == "socket_string":
                        self.string_data = recv_alldata
                    elif topic_name == "cmd_vel":
                        self.cmdvel_data = recv_alldata
                    elif topic_name == "odom":
                        self.odom_data = recv_alldata
                        print("收到odom数据为：",self.odom_data)
                    elif topic_name == "imu":
                        self.imu_data = recv_alldata
                    self.dataLock.release()
            except:
                pass
        

    #接受发送的速度数据
    def recv_cmdvel(self):
        linear_x=self.cmdvel_data["linear_x"]
        linear_y=self.cmdvel_data["linear_y"]
        angular_z=self.cmdvel_data["angular_z"]
        #self.cmdvel_data["linear_x"]=0
        #self.cmdvel_data["linear_y"]=0
        #self.cmdvel_data["angular_z"]=0
        return linear_x,linear_y,angular_z
        
    #接受里程计数据
    def recv_odom(self):
        linear_x=self.odom_data["linear_x"]
        linear_y=self.odom_data["linear_y"]
        angular_z=self.odom_data["angular_z"]
        # self.odom_data["linear_x"]=0
        # self.odom_data["linear_y"]=0
        # self.odom_data["angular_z"]=0
        return linear_x,linear_y,angular_z

    #接受imu数据
    def recv_imu(self):
        linear_x=self.imu_data["linear_x"]
        linear_y=self.imu_data["linear_y"]
        angular_z=self.imu_data["angular_z"]
        # self.imu_data["linear_x"]=0
        # self.imu_data["linear_y"]=0
        # self.imu_data["angular_z"]=0
        return linear_x,linear_y,angular_z
    def recv_string(self):
        #print("string_data:",self.string_data)
        data=self.string_data["data"]
        self.string_data["data"]=""
        return data

    #发布字符串
    def sent_string(self,msg):
        dataindex = self.topic_list.index("socket_string")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        data["data"]=msg#将要发送的数据赋值
        str_jsonstr = json.dumps(data)#将数据转化为字符串
        print("发送的信息为：",str_jsonstr)
        self.dataSocket.send(str_jsonstr.encode())#发布数据

    #发布速度
    def sent_vel(self,linear_x,linear_y,angular_z):
        dataindex = self.topic_list.index("cmd_vel")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        data["linear_x"]=linear_x#将要发送的数据赋值
        data["linear_y"]=linear_y
        data["angular_z"]=angular_z
        vel_jsonstr = json.dumps(data)#将数据转化为字符串
        print("发送的信息为：",vel_jsonstr)
        try:
            self.dataSocket.send(vel_jsonstr.encode())#发布数据
        except:
            print("未连接socket")

        
    #发布坐标点
    def sent_point(self,point_x,point_y,point_angle):
        dataindex = self.topic_list.index("move_base/goal")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        data["point_x"]=point_x#将要发送的数据赋值
        data["point_y"]=point_y
        data["point_angle"]=point_angle
        point_jsonstr = json.dumps(data)#将数据转化为字符串
        print("发送的信息为：",point_jsonstr)
        self.dataSocket.send(point_jsonstr.encode())#发布数据