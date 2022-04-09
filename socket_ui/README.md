## socket_ui : 实现window与ROS通信的可视化中央调度系统
---

## 运行环境
python3.6
Qt5 Version Number is: 5.15.2
PyQt5 Version is: 5.15.6

## 使用方法
直接运行ui_menu.py

## 实现功能
1.与ROS系统进行话题互传，目前支持cmd_vel,imu,move_base/goal,string等话题的互传，同时封装在socket_client库中，话题格式统一使用json格式文件报存，非常方便增加其它话题文件
2.能对ROS中速度信息进行可视化显示，方便参数调试和可视化分析
3.能调用摄像头数据，并调节亮度和对比度等信息，方便视觉进行调试

