# socketclient库使用教程

## 安装库

## 库的导入和实例化

**导入库**

```python
from socketclient import socket_client
```

**实例化库**

```python
sockclient=socket_client.SocketClient() 
```

## 启动/关闭连接函数

**开始连接，IP和PORT分别是服务端的IP地址和端口号**

```python
sockclient.open_connect(IP,PORT)#开始连接
```

**断开连接，IP和PORT分别是服务端的IP地址和端口号**

```python
sockclient.close_connect()
```


sockclient.sent_string(data)

## 发送数据函数

**发送字符串 数据为data**

```python
sockclient.sent_string(data)
```

**发送速度话题 vx,vy,va分别为小车x方向速度，y方向速度，角速度**

```python
sockclient.sent_vel(vx,vy,va)
```

**发送目标坐标点 px,py,pa分别为x坐标，y坐标和目标偏航角**

```python
sockclient.sent_point(px,py,pa)
```


## 接受数据函数

**接受字符串 返回数据为data**

```python
sockclient.recv_string()
```

**发送速度话题 返回数据为小车x方向速度，y方向速度，角速度**

```python
sockclient.recv_cmdvel()
```

**发送目标坐标点 返回数据为x坐标，y坐标和目标偏航角**

```python
sockclient.recv_odom(px,py,pa)
```
```







