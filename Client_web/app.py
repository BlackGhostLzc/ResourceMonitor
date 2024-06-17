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


def real_time_updater(cid, host_name, request_command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
        s.sendall(json.dumps({"node": "client", }).encode('utf-8'))
        time.sleep(0.01)
        while status[cid]:
            central_server_request = {
                "node": "client",
                "cmd": request_command,  # Can be "cpuinfo", "meminfo", "diskinfo" or "procinfo"
                "name": host_name,
            }
            s.sendall(json.dumps(central_server_request).encode('utf-8'))
            recvdata = s.recv(2048)
            return_data = json.loads(recvdata.decode('utf-8'))
            socketio.emit('update', return_data, room=cid)
            print("Sent\n")
            time.sleep(1)
    except socket.error as e:
        raise e
    finally:
        s.close()


status = {}
threads = {}


@socketio.on('connect')
def handle_connection():
    cid = request.sid
    hostname = request.args.get('host_name')
    request_command = request.args.get('request_command')
    print(f'Client {cid} connected with request hostname {hostname}')
    thread = threading.Thread(target=real_time_updater, args=(cid, hostname, request_command))
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




@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ls')
def ls():
    data = get_ls()
    return render_template('ls.html', data=data)


@app.route('/cpuinfo/<host_name>')
def cpuinfo(host_name):
    return render_template('cpuinfo.html', host_name=host_name)


@app.route('/meminfo/<host_name>')
def meminfo(host_name):
    return render_template('meminfo.html', host_name=host_name)


@app.route('/diskinfo/<host_name>')
def diskinfo(host_name):
    return render_template('diskinfo.html', host_name=host_name)


@app.route('/procinfo/<host_name>')
def procinfo(host_name):
    return render_template('procinfo.html', host_name=host_name)


@app.route('/overview/<host>')
def overview(host):
    return render_template('overview.html', host=host)


# Custom filter to replace underscores with spaces and capitalize the first letter
@app.template_filter('format_label')
def format_label(value):
    return value.replace('_', ' ').capitalize()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=36801)
