from server import AgentNodes
from server import agentNodesLock

import pickle
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
# 7. 获取进程process有关信息 procinfo hostname\

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


# server端的命令
# 向 agent 发送心跳 cmd = heartbeat

