import threading
import time

from flask import Flask, render_template, request
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_level_808'
socketio = SocketIO(app)


continue_status = {}
threads = {}


def send_message(message, cid):
    socketio.emit('message', {'data': message}, room=cid)

def looping_thread(cid):
    for i in range(100):
        if continue_status[cid]:
            send_message(str(i), cid)
            time.sleep(1)
        else:
            break

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    cid = request.sid
    print(f'Client {cid} connected')
    thread = threading.Thread(target=looping_thread, args=(cid,))
    threads[cid] = thread
    continue_status[cid] = True
    thread.start()
    print("Starting Real-time Updating")


@socketio.on('disconnect')
def handle_disconnect():
    cid = request.sid
    print(f'Client {cid} disconnected')
    continue_status[cid] = False
    threads[cid].join()
    del continue_status[cid]
    del threads[cid]
    print("Real-time-updating ends")

@socketio.on('stop_event')
def handle_stop_event(msg):
    cid = request.sid
    print(f"Received a stop event. Msg content: {msg}")
    global continue_status
    continue_status[cid] = False



if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8080)
