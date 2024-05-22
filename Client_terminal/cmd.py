import json
import pickle
import display
# 1. 获取服务端监控所有的主机 ls
# 输出  hostname         ip
#       24273        127.0.0.1
#       ....           .....
# 2. 获取某台主机的cpu有关信息 cpuinfo hostname
# 3. 获取某台主机的memory有关信息 meminfo hostname
# 4. 获取某台主机的disk有关信息 diskinfo hostname
# 5. 获取某台主机的network有关信息 netinfo hostname
# 6. 获取传感器sensors的有关信息 sensorinfo hostname
# 7. 获取进程process有关信息 procinfo hostname

def ls(conn):
    data = {
        "node": "client",
        "cmd": "ls",
    }
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)

    # 接收服务器的数据，这是一个二维的 list
    recvdata = conn.recv(1024)
    list = pickle.loads(recvdata)

    # TODO()
    # 炫酷输出
    display.displayLs(list)
    print(list)


def cpuinfo(conn, hostname):
    data = {
        "node": "client",
        "cmd": "cpuinfo",
        "name": hostname,
    }
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)
    recvdata = conn.recv(2048)
    cpuInfo = json.loads(recvdata.decode('utf-8'))
    print(cpuInfo)

    return

def meminfo(conn, hostname):
    data = {
        "node": "client",
        "cmd": "meminfo",
        "name": hostname,
    }
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)
    recvdata = conn.recv(2048)
    memInfo = json.loads(recvdata.decode('utf-8'))
    print(memInfo)


def diskinfo(conn, hostname):
    data = {
        "node": "client",
        "cmd": "diskinfo",
        "name": hostname,
    }
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)
    recvdata = conn.recv(2048)
    diskInfo = json.loads(recvdata.decode('utf-8'))
    print(diskInfo)


def netinfo(conn, hostname):
    pass

def sensorinfo(conn, hostname):
    data = {
        "node": "client",
        "cmd": "sensorinfo",
        "name": hostname,
    }
    message = json.dumps(data).encode('utf-8')
    conn.sendall(message)
    recvdata = conn.recv(2048)
    sensorInfo = json.loads(recvdata.decode('utf-8'))
    print(sensorInfo)


def procinfo(conn, hostname):
    pass


command_mapping = {
    "ls": ls,
    "cpuinfo": cpuinfo,
    "meminfo": meminfo,
    "diskinfo": diskinfo,
    "netinfo": netinfo,
    "sensorinfo": sensorinfo,
    "procinfo": procinfo,
}
