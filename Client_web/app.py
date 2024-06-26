from flask import Flask, render_template, jsonify
import socket
import json
import pickle
import os

app = Flask(__name__)

def get_host_address():
    # 获取本机主机名
    host = socket.gethostname()
    # 获取本机IP地址
    ip_address = socket.gethostbyname(host)
    return ip_address


HOST = get_host_address()  # 服务器IP地址
PORT = 65432  # 服务器端口
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# 发送身份信息
data = {
    "node": "client",
}
message = json.dumps(data).encode('utf-8')
s.sendall(message)


def get_ls():
    try:
        data = {
            "node": "client",
            "cmd": "ls",
        }
        message = json.dumps(data).encode('utf-8')
        s.sendall(message)
        # 接收服务器的数据，这是一个二维的 list
        recvdata = s.recv(1024)
        list = pickle.loads(recvdata)
        print(list)
        return list
    except socket.error as e:
        return {"error": str(e)}


# Custom filter to replace underscores with spaces and capitalize the first letter
@app.template_filter('format_label')
def format_label(value):
    return value.replace('_', ' ').capitalize()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ls')
def ls():
    data = get_ls()
    return render_template('ls.html', data=data)


@app.route('/cpuinfo/<host>')
def cpuinfo(host):
    # 这里可以根据实际需要获取更多关于主机的信息
    data = {
        "node": "client",
        "cmd": "cpuinfo",
        "name": host,
    }
    message = json.dumps(data).encode('utf-8')
    s.sendall(message)
    recvdata = s.recv(2048)
    data = json.loads(recvdata.decode('utf-8'))
    print(data)
    return render_template('cpuinfo.html', data=data)


@app.route('/meminfo/<host>')
def meminfo(host):
    # 这里可以根据实际需要获取更多关于主机的信息
    data = {
        "node": "client",
        "cmd": "meminfo",
        "name": host,
    }
    message = json.dumps(data).encode('utf-8')
    s.sendall(message)
    recvdata = s.recv(2048)
    data = json.loads(recvdata.decode('utf-8'))
    print(data)
    return render_template('meminfo.html', memory_info=data)


@app.route('/diskinfo/<host>')
def diskinfo(host):
    # 这里可以根据实际需要获取更多关于主机的信息
    data = {
        "node": "client",
        "cmd": "diskinfo",
        "name": host,
    }
    message = json.dumps(data).encode('utf-8')
    s.sendall(message)
    recvdata = s.recv(2048)
    data = json.loads(recvdata.decode('utf-8'))
    print(data)
    return render_template('diskinfo.html', disk_info=data)


@app.route('/procinfo/<host>')
def procinfo(host):
    # 这里可以根据实际需要获取更多关于主机的信息
    data = {
        "node": "client",
        "cmd": "procinfo",
        "name": host,
    }
    message = json.dumps(data).encode('utf-8')
    s.sendall(message)
    recvdata = s.recv(2048)
    data = json.loads(recvdata.decode('utf-8'))
    print(data)
    return render_template('procinfo.html', procList=data["procinfo"])


if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=36801)  # 客户端在端口 5000 上运行
    finally:
        s.close()  # 确保应用退出时关闭 socket
