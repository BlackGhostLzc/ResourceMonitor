import socket
import threading
import time
import pickle
import util
import json

# 服务器地址和端口
HOST = '127.0.0.1'
PORT = 65432

agentNodesLock = threading.Lock()

AgentNodes = []

def handleAgent(conn, cmd, name, addr):
    # 首先需要把监控的主机记录下来
    # 需要把连接 conn 记录下来
    node = util.Node(name, conn, addr)

    agentNodesLock.acquire()
    AgentNodes.append(node)
    agentNodesLock.release()
    print("A new agent comes in")

    # 发送连接成功相应
    response = "ok"
    conn.sendall(response.encode())
    while(True):
        # 发送 HeartBeat
        command = {
            "node": "server",
            "cmd": "heartbeat",
        }
        message = json.dumps(command).encode('utf-8')
        conn.sendall(message)
        # 如果相应不成功怎么办
        # TODO(),需要从 AgentNodes 中去除这个 node
        # 每隔 5 秒发送 1 次心跳
        time.sleep(5)

    return

def handleClientLs(conn):
    agentNodesLock.acquire()
    # 发送所有 agent 的信息给client
    table_data = []
    for node in AgentNodes:
        tuple = []
        tuple.append(node.name)
        tuple.append(node.addr)
        table_data.append(tuple)

    agentNodesLock.release()
    conn.sendall(pickle.dumps(table_data))


def handleClient(conn):
    # 这个线程负责处理所有和 client 的交互
    while True:
        # 不断读取用户的输入命令
        message = conn.recv(1024)
        command = json.loads(message.decode('utf-8'))
        # 判断 client 命令的类型
        # 这是一个 json 类型的格式

        if command["cmd"] == "ls":
            handleClientLs(conn)
        elif command["cmd"] == "cpuinfo":
            continue

        elif command["cmd"] == "meminfo":
            continue

        elif command["cmd"] == "diskinfo":
            continue

        elif command["cmd"] == "procinfo":
            continue

        elif command["cmd"] == "sensorinfo":
            continue

        elif command["cmd"] == "netinfo":
            continue


    return


def handleConn(conn, addr):
    with conn:
        # data 是字节流
        message = conn.recv(1024)
        command = json.loads(message.decode('utf-8'))

        # 这个 command 可能是客户端的命令，可能是 agent 的连接命令
        # 如果是 agent 的连接命令则需要专门创建 1 个线程负责和 client 进行交互
        print(command)

        if command["node"] == "agent":
            handleAgent(conn, cmd=command["cmd"], name=command["name"], addr = addr)
        elif command["node"] == "client":
            handleClient(conn)


# 创建一个套接字对象
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 将套接字绑定到指定的地址和端口
    s.bind((HOST, PORT))
    # 开始监听连接
    s.listen()

    print("Server is listening...")

    # 开启一个线程，向所有 agent 发送心跳
    # heartbeatThread = threading.Thread(target=broadcastHeartBeat)
    # heartbeatThread.start()

    while True:
        # 接受客户端连接
        conn, addr = s.accept()

        # 开启一个新的线程处理这个连接
        thread = threading.Thread(target=handleConn, args=(conn,addr))
        thread.start()