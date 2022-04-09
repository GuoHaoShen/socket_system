#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from ast import Pass
from socket import *
import json
from threading import Thread,Lock
from time import sleep
import rospy
#导入ros消息类型库
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point,PoseWithCovarianceStamped
from move_base_msgs.msg import MoveBaseActionGoal
#from tf_conversions import transformations
from math import pi
from math import sin
from math import cos

class SocketServer():
    def __init__(self,IP,PORT):
        self.read_json() 
        self.open_node()
        #self.open_connect(IP,PORT)   
        # self.init_subscriber()
        #self.dataLock = Lock()

    #初始化节点
    def open_node(self):
            print("初始化节点")
            rospy.init_node("socket_server")
            self.string_pub = rospy.Publisher("socket_string",String,queue_size=10)        
            self.point_pub = rospy.Publisher("move_base/goal",MoveBaseActionGoal,queue_size=10)        
            self.cmd_vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)        

            # self.string_sub = rospy.Subscriber("socket_string",String,self.string_callback,queue_size=10)
            # self.imu_sub = rospy.Subscriber("imu",Imu,self.imu_callback,queue_size=10)
            # self.odom_sub = rospy.Subscriber("odom",Odometry,self.odom_callback,queue_size=10)
            # self.cmd_vel_sub = rospy.Subscriber("cmd_vel",Twist,self.cmd_vel_callback,queue_size=10)
    def init_subscriber(self):
            self.string_sub = rospy.Subscriber("socket_string_ros",String,self.string_callback,queue_size=1)
            self.imu_sub = rospy.Subscriber("imu",Imu,self.imu_callback,queue_size=1)
            self.odom_sub = rospy.Subscriber("odom",Odometry,self.odom_callback,queue_size=1)
            self.cmd_vel_sub = rospy.Subscriber("cmd_vel",Twist,self.cmd_vel_callback,queue_size=1)       

    #开启连接
    def open_connect(self,IP,PORT):
        # 实例化一个socket对象，指明协议
        self.listenSocket = socket(AF_INET, SOCK_STREAM)
        # 连接客户端socket
        self.listenSocket.bind((IP, PORT))
        # 监听链接
        self.listenSocket.listen(128)
        print("服务端开启完成，等待客户端连接中.......")
         # 4.接收别人的连接
        self.dataSocket, addr = self.listenSocket.accept()
        print('接受一个客户端连接:', addr)


    #关闭连接
    def close_connect(self):
        print("结束通信！")
        self.dataSocket.close()
        self.listenSocket.close()


    #读取json文件
    def read_json(self):
        #with open("../socket_server/config/wtopic.json",'r') as load_f:
        with open("/home/pricen/catkin_ws/src/socket_server/config/wtopic.json",'r') as load_f:
            self.wtopic = json.load(load_f)
            print("成功读取数据类型文件")
        self.topic_list = [] #话题名列表
        #导入话题名列表
        for i in range(len(self.wtopic)):
            self.topic_list.append(self.wtopic[i]["topic_name"])

    def recv_all(self):
        recv_alldata = self.dataSocket.recv(1024)
        # if not recv_alldata:
        #     break
        recv_alldata = json.loads(recv_alldata.decode())
        print("数据类型为：",type(recv_alldata))
        print("recv_alldata : ",recv_alldata)
        if recv_alldata["topic_name"] in self.topic_list:
            topic_name=recv_alldata["topic_name"]

            if topic_name == "socket_string":
                self.pub_string(recv_alldata)
            elif topic_name == "cmd_vel":
                self.pub_cmdvel(recv_alldata)
            elif topic_name == "move_base/goal":
                self.pub_point(recv_alldata)
        

    #接受发送的速度数据
    def pub_cmdvel(self,data):
        msg = Twist()
        msg.linear.x=float(data["linear_x"])
        msg.linear.y=float(data["linear_y"])
        msg.linear.z=0
        msg.angular.z=float(data["angular_z"])
        self.cmd_vel_pub.publish(msg)
        print("发布cmdvel成功！")

        
    #接受坐标点数据
    def pub_point(self,msg):
        x,y,th=msg["point_x"],msg["point_y"],msg["point_angle"]
        pose = MoveBaseActionGoal()
        pose.header.stamp = rospy.Time.now()
        pose.goal.target_pose.header.frame_id = 'map'
        pose.goal.target_pose.pose.position.x = float(x)
        pose.goal.target_pose.pose.position.y = float(y)
        #q = transformations.quaternion_from_euler(0.0, 0.0, th/180.0*pi)
        q = self.rpy2quaternion(0.0, 0.0, float(th)/180.0*pi)
        pose.goal.target_pose.pose.orientation.x = q[0]
        pose.goal.target_pose.pose.orientation.y = q[1]
        pose.goal.target_pose.pose.orientation.z = q[2]
        pose.goal.target_pose.pose.orientation.w = q[3]
        self.point_pub.publish(pose)
        print("发布point成功！")

    #接受imu数据
    def pub_string(self,data):
        # #将接受的话题发布
        msg = String()
        msg.data = data["data"]
        self.string_pub.publish(msg)
        print("发布string成功！")


    def string_callback(self,msg):
        dataindex = self.topic_list.index("socket_string")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        data["data"]=msg.data       #将要发送的数据赋值
        str_jsonstr = json.dumps(data)#将数据转化为字符串
        self.dataSocket.send(str_jsonstr.encode())#发布数据
        print ("收到string话题并发布!")
    
    def imu_callback(self,msg):
        pass

    def odom_callback(self,msg):
        dataindex = self.topic_list.index("odom")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        #print ('数据data',data)
        data["linear_x"]=msg.twist.twist.linear.x
        data["linear_y"]=msg.twist.twist.linear.y
        data["angular_z"]=msg.twist.twist.angular.z
        #print ('数据data',data)
        odom_jsonstr = json.dumps(data)#将数据转化为字符串
        self.dataSocket.send(odom_jsonstr.encode())#发布数据
        print ("收到odom话题并发布,vx:",data["linear_x"])
       # print (odom_jsonstr.encode())
        sleep(0.15)

    def cmd_vel_callback(self,msg):
        dataindex = self.topic_list.index("cmd_vel")
        data = self.wtopic[dataindex]#初始化发送的数据类型
        data["linear_x"]=msg.linear.x       #将要发送的数据赋值
        data["linear_y"]=msg.linear.y
        data["angular_z"]= msg.angular.z
        str_jsonstr = json.dumps(data)#将数据转化为字符串
        self.dataSocket.send(str_jsonstr.encode())#发布数据
        print ("收到cmd_vel话题并发布!")
        sleep(0.15)
    
    #欧拉角转四元素
    def rpy2quaternion(self,roll, pitch, yaw):
        x=sin(pitch/2)*sin(yaw/2)*cos(roll/2)+cos(pitch/2)*cos(yaw/2)*sin(roll/2)
        y=sin(pitch/2)*cos(yaw/2)*cos(roll/2)+cos(pitch/2)*sin(yaw/2)*sin(roll/2)
        z=cos(pitch/2)*sin(yaw/2)*cos(roll/2)-sin(pitch/2)*cos(yaw/2)*sin(roll/2)
        w=cos(pitch/2)*cos(yaw/2)*cos(roll/2)-sin(pitch/2)*sin(yaw/2)*sin(roll/2)
        return x, y, z, w


if __name__ == "__main__":
        IP="192.168.119.146"
        PORT=8000
        sserver=SocketServer(IP,PORT) 
        print("开始连接")
        print("self addr :",IP)
        print("self addr :",PORT)
        sserver.open_connect(IP,PORT)
        sserver.init_subscriber()
        while not rospy.is_shutdown():
                #接受数据并进行处理
                print("开始读取数据")
                sserver.recv_all()

