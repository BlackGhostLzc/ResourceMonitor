import json
import pickle

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
    print(list)


def cpuinfo(conn, hostname):

    pass

def meminfo(conn, hostname):
    pass

def diskinfo(conn, hostname):
    pass

def netinfo(conn, hostname):
    pass

def sensorinfo(hostname):
    pass

def procinfo(hostname):
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
