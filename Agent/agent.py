import socket
import psutil
import json

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
        "type": "agent",
        "cmd": "monitored",
        "name": hostname,
    }

    message = json.dumps(data).encode('utf-8')
    s.sendall(message)


    # 不断相应服务器获取硬件资源的请求
    # while True:
    #    recvdata = s.recv(1024)











