from flask import Flask, render_template, request
import socket
import json
import pickle
from flask_socketio import SocketIO
import threading
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_level_808'
socketio = SocketIO(app)

def get_host_address():
    # 获取本机主机名
    host = socket.gethostname()
    # 获取本机IP地址
    ip_address = socket.gethostbyname(host)
    return ip_address

HOST = get_host_address()  # 服务器IP地址, which means that the server and the Flask app should be on the same machine
PORT = 65432  # 服务器端口




def get_ls():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.sendall(json.dumps({"node": "client", }).encode('utf-8'))
        time.sleep(0.01)
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
    finally:
        s.close()



def real_time_cpu(cid, hostname):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.sendall(json.dumps({"node": "client", }).encode('utf-8'))
        time.sleep(0.01)
        while status[cid]:
            central_server_request = {
                "node": "client",
                "cmd": "cpuinfo",
                "name": hostname,
            }
            request_message = json.dumps(central_server_request).encode('utf-8')
            s.sendall(request_message)
            recvdata = s.recv(2048)
            return_data = json.loads(recvdata.decode('utf-8'))
            # return_data = {
            #     "cpu_count": 2,
            #     "cpu_percent": [30, 20],
            #     "cpu_times": '1',
            #     "cpu_freq": "2",
            #     "cpu_stats": "3",
            # }
            socketio.emit('updateCPUInfo', return_data, room=cid)
            print("Sent\n")
            time.sleep(0.5)
    except socket.error as e:
        raise e
    finally:
        s.close()




status = {}
threads = {}

@socketio.on('connect')
def handle_connection():
    hostname = request.args.get('hostname')
    cid = request.sid
    print(f'Client {cid} connected with request hostname {hostname}')
    thread = threading.Thread(target=real_time_cpu, args=(cid, hostname))
    threads[cid] = thread
    status[cid] = True
    thread.start()
    print("Starting Real-time Updating")


@socketio.on('disconnect')
def handle_disconnect():
    cid = request.sid
    print(f'Client {cid} disconnected')
    status[cid] = False
    threads[cid].join()
    del status[cid]
    del threads[cid]
    print("Real-time-updating ends")














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
    return render_template('cpuinfo.html', host=host)


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
    app.run(host='127.0.0.1', port=36801)
