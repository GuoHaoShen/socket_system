## 名称：中央任务调度系统

## 版本号：1.0

## 开发者：华南农业大学Taurus战队队员

## 开发工具：python+pyqt5+Qtdesigner+socket

## 运行环境
### 客户端
python3.6
Qt5 Version Number is: 5.15.2
PyQt5 Version is: 5.15.6
### 服务端
ubuntu18.04

## 功能模块：中央调度系统，中央监控系统，中央通信系统，视觉调试工具

## 实现的功能：
1.与ROS系统进行话题互传，目前支持cmd_vel,imu,move_base/goal,string等话题的互传，同时封装在socket_client库中，话题格式统一使用json格式文件报存，非常方便增加其它话题文件
2.能对ROS中速度信息进行可视化显示，方便参数调试和可视化分析
3.能调用摄像头数据，并调节亮度和对比度等信息，方便视觉进行调试

## 使用方法：
1.socket_server文件放在Ubuntu端，socket_ui文件放在window端，保证在同一局域网
2.socket_server/src/socket_server.py文件中181行IP和端口改为实际IP
3.运行服务端socket_server.py文件，和客户端ui_menu.py文件
4.输入服务端显示的ip地址和端口号port，点击连接即可

## 常见问题：
1.连接失败且ping失败，检查IP、和port是否正确，检查防火墙，检查虚拟机网络设置
2.客户端找不到ui文件，检查终端路径是否为socket_ui（或将7个文件'uic.loadUi("ui/ui_camera.ui")'中路径改为绝对路径）
3.服务端意外断开连接后会卡死，需要重新启动（一个小bug，没来得及改，欢迎大家改进）

## 代码框架：
### 服务端
主程序为ui_menu.py文件，6个子窗口分别在其余6个*ui.py文件
ui文件夹包括各个ui文件和图片资源，socket_client包中为socket通信相关文件，config文件中为自定义的JSON文件
### 客户端
主程序为socket_server.py文件，调用自定义的JSON文件

## 写在最后
由于时间有限，本项目还有很大的改进空间，非常欢迎大家进行改进