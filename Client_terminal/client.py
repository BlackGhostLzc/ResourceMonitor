import socket
import psutil
import cmd
import json

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432

commandList = ["ls", "cpuinfo", "meminfo", "diskinfo", "netinfo", "sensorinfo", "procinfo"]

def handleCommand(command, conn):
    if len(command) < 1:
        print("Invalid command")
        return

    if command[0] not in cmd.command_mapping:
        print("Invalid command")
        return

    # 这是C语言中类似于函数指针
    f = cmd.command_mapping[command[0]]

    if command[0] == 'ls':
        f(conn)
    else:
        if len(command) < 2:
            print("Invalid command")
        f(conn,command[1])

    return

# 创建一个套接字对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("client connect to server success")

    # 初始化 command 的信息

    # 首先告诉 server 自己是一个 client
    data = {
        "node":"client",
    }
    message = json.dumps(data).encode('utf-8')
    s.sendall(message)

    while True:
        user_input = input("sh> ")
        command = user_input.split()

        # 如果 command 不是我们内置的一些命令
        if command[0] not in commandList:
            print("Invalid command")
            continue

        # quit 退出
        if command[0] == "quit":
            print("bye~~~")
            break

        # words[0] 为命令，后面的就是参数
        handleCommand(command, s)



