import socket
import threading
import time
import pickle
import json

import cmd
import util

# 服务器地址和端口
HOST = '192.168.56.1'
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

def handleClientCpuInfo(conn, hostname):
    # 1.从 AgentNodes 中找到对应的连接和主机
    agentNodesLock.acquire()
    agentConn = None
    for node in AgentNodes:
        if node.name == hostname:
            agentConn = node.conn
            break
    agentNodesLock.release()

    if agentConn is None:
        print("No such an agent")
        conn.sendall("No such an agent")
        return

    # 2.然后通过 hostconn 向被监控的主机发送命令 cpuinfo
    print("服务器准备获取 agent 的 cpu 数据")

    cpuInfo = cmd.requireCpuInfoFromAgent(agentConn)
    print(cpuInfo)

    # 3.得到数据后发送给 conn 客户端
    conn.sendall(json.dumps(cpuInfo).encode('utf-8'))


def handleClientMemInfo(conn, hostname):
    # 1.从 AgentNodes 中找到对应的连接和主机
    agentNodesLock.acquire()
    agentConn = None
    for node in AgentNodes:
        if node.name == hostname:
            agentConn = node.conn
            break
    agentNodesLock.release()

    if agentConn is None:
        print("No such an agent")
        conn.sendall("No such an agent")
        return

    # 2.然后通过 hostconn 向被监控的主机发送命令 cpuinfo
    print("服务器准备获取 agent 的 mem 数据")

    memInfo = cmd.requireMemInfoFromAgent(agentConn)
    print(memInfo)

    # 3.得到数据后发送给 conn 客户端
    conn.sendall(json.dumps(memInfo).encode('utf-8'))

def handleClientDiskInfo(conn, hostname):
    # 1.从 AgentNodes 中找到对应的连接和主机
    agentNodesLock.acquire()
    agentConn = None
    for node in AgentNodes:
        if node.name == hostname:
            agentConn = node.conn
            break
    agentNodesLock.release()

    if agentConn is None:
        print("No such an agent")
        conn.sendall("No such an agent")
        return

    # 2.然后通过 hostconn 向被监控的主机发送命令 cpuinfo
    print("服务器准备获取 agent 的 disk 数据")

    diskInfo = cmd.requireDiskInfoFromAgent(agentConn)
    print(diskInfo)

    # 3.得到数据后发送给 conn 客户端
    conn.sendall(json.dumps(diskInfo).encode('utf-8'))


def handleClientProcInfo(conn, hostname):
    agentNodesLock.acquire()
    agentConn = None
    for node in AgentNodes:
        if node.name == hostname:
            agentConn = node.conn
            break
    agentNodesLock.release()

    if agentConn is None:
        print("No such an agent")
        conn.sendall("No such an agent")
        return

    # 2.然后通过 hostconn 向被监控的主机发送命令 cpuinfo
    print("服务器准备获取 agent 的 proc 数据")

    procInfo = cmd.requireProcInfoFromAgent(agentConn)
    print(procInfo)
    # 3.得到数据后发送给 conn 客户端
    conn.sendall(json.dumps(procInfo).encode('utf-8'))



def handleClientSensorInfo(conn, hostname):
    # 1.从 AgentNodes 中找到对应的连接和主机
    agentNodesLock.acquire()
    agentConn = None
    for node in AgentNodes:
        if node.name == hostname:
            agentConn = node.conn
            break
    agentNodesLock.release()

    if agentConn is None:
        print("No such an agent")
        conn.sendall("No such an agent")
        return

    # 2.然后通过 hostconn 向被监控的主机发送命令 cpuinfo
    print("服务器准备获取 agent 的 sensor 数据")

    sensorInfo = cmd.requireSensorInfoFromAgent(agentConn)
    print(sensorInfo)

    # 3.得到数据后发送给 conn 客户端
    conn.sendall(json.dumps(sensorInfo).encode('utf-8'))

def handleClientNetInfo(conn, hostname):
    pass

def handleClient(conn):
    # 这个线程负责处理所有和 client 的交互
    print("A new client comes in")
    while True:
        # 不断读取用户的输入命令
        message = conn.recv(1024)

        # 用户的输入是什么？ 是 1 个 json 字符串
        command = json.loads(message.decode('utf-8'))
        print(command)
        # 判断 client 命令的类型
        # 这是一个 json 类型的格式

        if command["cmd"] == "ls":
            handleClientLs(conn)
        elif command["cmd"] == "cpuinfo":
            handleClientCpuInfo(conn, command["name"])

        elif command["cmd"] == "meminfo":
            handleClientMemInfo(conn, command["name"])
            continue

        elif command["cmd"] == "diskinfo":
            handleClientDiskInfo(conn, command["name"])
            continue

        elif command["cmd"] == "procinfo":
            handleClientProcInfo(conn, command["name"])
            continue

        elif command["cmd"] == "sensorinfo":
            print("server收到一个client sensor")
            handleClientSensorInfo(conn, command["name"])
            continue

        elif command["cmd"] == "netinfo":
            handleClientNetInfo(conn, command["name"])
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


def listen_for_broadcast():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_sock.bind(('', 12345))  # 12345 是广播端口

    print("Server listening for broadcasts on port 12345")

    while True:
        data, addr = udp_sock.recvfrom(1024)
        if data.decode() == "agent_address":
            print(f"Received broadcast from {addr}")
            start_tcp_connection_agent(addr[0])

def start_tcp_connection_agent(agent_host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
        agent_port = 54321  # 客户端监听的端口
        tcp_sock.connect((agent_host, agent_port))

        response = tcp_sock.recv(1024).decode()
        if response != "ok":
            print("Connect to agent failed")
            exit(1)
        # 成功接受后
        print("connect to agent success")
        handleAgent(tcp_sock, cmd="cmd", name="name", addr=(agent_host, agent_port))




def start_tcp_connection_client():

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

client_thread = threading.Thread(target=start_tcp_connection_client)
broadcast_thread = threading.Thread(target=listen_for_broadcast)

# 启动线程
client_thread.start()
broadcast_thread.start()


# 等待线程完成
broadcast_thread.join()
client_thread.join()