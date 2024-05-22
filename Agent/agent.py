import socket
import psutil
import json

import resource

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432

# 创建一个套接字对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 主动连接到服务器
    s.connect((HOST, PORT))

    # 连接服务器
    userinfo = psutil.users()
    hostname = userinfo[0][0]

    data = {
        "node": "agent",
        "cmd": "monitored",
        "name": hostname,
    }

    message = json.dumps(data).encode('utf-8')
    s.sendall(message)

    response = s.recv(1024).decode()
    if response != "ok":
        print("Connect to server failed")
        exit(1)

    # 成功接受后
    print("connect to server success")

    # 不断相应服务器获取硬件资源的请求
    while True:
        # 接受服务器发送的资源请求或者是心跳
        recvdata = s.recv(1024)
        print(recvdata)
        command = json.loads(recvdata.decode('utf-8'))

        # 如果是心跳
        if command["cmd"] == "heartbeat":
            # print("收到 1 个心跳")
            pass

        if command["cmd"] == "cpuinfo":
            # 获取相关的资源并发送
            data = resource.requireCpuInfo()
            print(data)
            message = json.dumps(data).encode('utf-8')
            s.sendall(message)

        elif command["cmd"] == "meminfo":
            # 获取相关的资源并发送
            data = resource.requireMemInfo()
            print(data)
            message = json.dumps(data).encode('utf-8')
            s.sendall(message)

        elif command["cmd"] == "diskinfo":
            data = resource.requireDiskInfo()
            print(data)
            message = json.dumps(data).encode('utf-8')
            s.sendall(message)

        elif command["cmd"] == "sensorinfo":
            data = resource.requireSensorInfo()
            print(data)
            message = json.dumps(data).encode('utf-8')
            s.sendall(message)

        # 可能是需要硬件资源信息

        # 如果是资源的请求













