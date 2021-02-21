from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import zmq
import threading
import time
#import socket

#Flask Crap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

context = zmq.Context()

#  Socket to talk to server
socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.200:5555") #!!!!!!!!!!!!!!!!!!!!!!!!!!!!! Replace with Raspberry Pi IP

@app.route('/')
def index():
    return render_template('index.html')

@socketio.event()
def update(message):
    print("Updating")
    socket.send_string("update")
    time.sleep(0.1)
    ZMQmessage = socket.recv_string()
    if(ZMQmessage == "Arrived"):
        emit('status_update', {'data': "Base"})
    elif(ZMQmessage == "Idle"):
        emit('status_update', {'data': "Idle"})


@socketio.event()
def Call(message):
    ZMQmessage = "Lmao"
    while(ZMQmessage != "Recieved"):
        socket.send_string("A1")
        #  Get the reply.
        time.sleep(1)
        ZMQmessage = socket.recv_string()
        print(ZMQmessage)
    emit('status_update', {'data': "Moving"})

@socketio.event()
def Return(message):
    ZMQmessage = "Lmao"
    while(ZMQmessage != "Return"):
        socket.send_string("Return")
        #  Get the reply.
        time.sleep(1)
        ZMQmessage = socket.recv_string()
    emit('status_update', {'data': "Moving"})


@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})

@socketio.on('connect')
def test_connect():
    print("connected")
    emit('my response', {'data': 'Connected'})
    #return render_template('index.html', instruction="connected")

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)

