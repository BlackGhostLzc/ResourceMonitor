import socket
import time
import threading
import json

import resource

connect_state = 0

def broadcast_address():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    data = {
        "node": "agent",
        "cmd": "monitored",
        "name": socket.gethostname(),
    }

    message = json.dumps(data).encode('utf-8')

    broadcast_address = ('<broadcast>', 12345)  # 12345 是广播端口

    global connect_state
    try:
        while connect_state == 0 :
            udp_sock.sendto(message, broadcast_address)
            print("Broadcasting address...")
            time.sleep(5)  # 每隔5秒广播一次
    except KeyboardInterrupt:
        print("Stopping broadcast")
    finally:
        udp_sock.close()

def start_tcp_agent():
    host = '0.0.0.0'
    port = 54321  # 客户端监听的端口

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Client TCP server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()

            with conn:
                # 发送连接成功相应
                response = "ok"
                conn.sendall(response.encode())
                global connect_state
                connect_state = 1

                print(f"Connected by {addr}")
                while True:
                    recvdata = conn.recv(1024)
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
                        conn.sendall(message)

                    elif command["cmd"] == "meminfo":
                        # 获取相关的资源并发送
                        data = resource.requireMemInfo()
                        print(data)
                        message = json.dumps(data).encode('utf-8')
                        conn.sendall(message)

                    elif command["cmd"] == "diskinfo":
                        data = resource.requireDiskInfo()
                        print(data)
                        message = json.dumps(data).encode('utf-8')
                        conn.sendall(message)

                    elif command["cmd"] == "sensorinfo":
                        data = resource.requireSensorInfo()
                        print(data)
                        message = json.dumps(data).encode('utf-8')
                        conn.sendall(message)

                    elif command["cmd"] == "procinfo":
                        data = resource.requireProcInfo()
                        print(data)
                        message = json.dumps(data).encode('utf-8')
                        conn.sendall(message)

                    # 可能是需要硬件资源信息

                    # 如果是资源的请求

# 创建两个线程分别执行 broadcast_address 和 start_tcp_agent
broadcast_thread = threading.Thread(target=broadcast_address)
tcp_agent_thread = threading.Thread(target=start_tcp_agent)

# 启动线程
broadcast_thread.start()
tcp_agent_thread.start()

# 等待线程完成
broadcast_thread.join()
tcp_agent_thread.join()
