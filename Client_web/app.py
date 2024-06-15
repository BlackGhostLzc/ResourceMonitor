import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room
import socket
import json
import pickle
import threading


# Create HTML server app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Create a lock for the socket
socket_lock = threading.Lock()


# Custom filter to replace underscores with spaces and capitalize the first letter
@app.template_filter('format_label')
def format_label(value):
    return value.replace('_', ' ').capitalize()






def fetch_cpu_data(host_name):
    print("Starting to fetch data from certer server...")
    while True:
        try:
            _data = {
                "node": "client",
                "cmd": "cpuinfo",
                "name": host_name,
            }
            _message = json.dumps(_data).encode('utf-8')
            s.sendall(_message)
            print("Sent request...")
            recvdata = s.recv(2048)
            print("Recv...")
            recvdata_json = json.loads(recvdata.decode('utf-8'))
            print("Loaded as json...")

            socketio.emit('updateCpuData', recvdata_json, room=host_name)
            print("Emitted")
            time.sleep(0.5)  # Update every 0.5 seconds
        except socket.error as e:
            print(f"Socket error: {e}")
            break



@socketio.on('connect')
def handle_cpu_connect():
    host_name = request.args.get('host_name')
    print(f"Client connected for information about host: {host_name}")
    join_room(host_name)
    threading.Thread(target=fetch_cpu_data, args=(host_name,)).start()
























# Routes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ls')
def ls():
    _data = get_ls()
    return render_template('ls.html', data=_data)

def get_ls():
    try:
        _out_data = {
            "node": "client",
            "cmd": "ls",
        }
        _out_message = json.dumps(_out_data).encode('utf-8')
        s.sendall(_out_message)
        # 接收服务器的数据，这是一个二维的 list
        recvdata = s.recv(1024)
        _list = pickle.loads(recvdata)
        print(_list)
        return _list
    except socket.error as e:
        return {"error": str(e)}


@app.route('/cpuinfo/<host_name>')
def cpuinfo(host_name):
    return render_template('cpuinfo.html', host_name=host_name)


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











# Connect to center server
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




if __name__ == '__main__':
    try:
        socketio.run(app, host='127.0.0.1', port=36801, debug=False)
    finally:
        s.close()  # 确保应用退出时关闭socket
