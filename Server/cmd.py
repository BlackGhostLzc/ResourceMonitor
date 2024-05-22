import pickle
import json

# 支持的命令
# agent 端的命令
# 1. agent 只有一种命令, monitored hostname, hostname 是本主机的名称


# client 端的命令

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

# server端的命令
def requireCpuInfoFromAgent(agentConn):
    command = {
        "node": "server",
        "cmd": "cpuinfo",
    }
    message = json.dumps(command).encode('utf-8')
    agentConn.sendall(message)
    recvdata = agentConn.recv(2048)

    cpuInfo = json.loads(recvdata.decode('utf-8'))
    return cpuInfo

def requireMemInfoFromAgent(agentConn):
    command = {
        "node": "server",
        "cmd": "meminfo",
    }
    message = json.dumps(command).encode('utf-8')
    agentConn.sendall(message)
    recvdata = agentConn.recv(2048)

    memInfo = json.loads(recvdata.decode('utf-8'))
    return memInfo

def requireDiskInfoFromAgent(agentConn):
    command = {
        "node": "server",
        "cmd": "diskinfo",
    }
    message = json.dumps(command).encode('utf-8')
    agentConn.sendall(message)
    recvdata = agentConn.recv(2048)

    diskInfo = json.loads(recvdata.decode('utf-8'))
    return diskInfo

def requireSensorInfoFromAgent(agentConn):
    command = {
        "node": "server",
        "cmd": "sensorinfo",
    }
    message = json.dumps(command).encode('utf-8')
    agentConn.sendall(message)
    recvdata = agentConn.recv(2048)

    sensorInfo = json.loads(recvdata.decode('utf-8'))
    return sensorInfo