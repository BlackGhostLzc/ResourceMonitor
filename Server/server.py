import socket
import threading
import util
import json

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432


def handleAgent(conn, cmd, arg):
    return


def handleClient(conn, cmd, arg):
    return


def handleConn(conn, addr):
    with conn:
        # data 是字节流
        message = conn.recv(1024)
        command = json.loads(message.decode('utf-8'))

        # 这个 command 可能是客户端的命令，可能是 agent 的连接命令
        if command["type"] == "agent":
            handleAgent(conn, cmd=command["cmd"], arg=command["name"])

        elif command["type"] == "client":
            handleClient(conn, cmd=command["cmd"], arg=command["arg"])


# 创建一个套接字对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 将套接字绑定到指定的地址和端口
    s.bind((HOST, PORT))
    # 开始监听连接
    s.listen()

    print("Server is listening...")

    while True:
        # 接受客户端连接
        conn, addr = s.accept()

        # 开启一个新的线程处理这个连接
        thread = threading.Thread(target=handleConn, args=(conn,addr))
        thread.start()