from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import zmq
#import socket

#Flask Crap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

@app.route('/', defaults={"instruction": "Go"})
@app.route('/<instruction>')
def index(instruction):
    return render_template('index.html', instruction=instruction)

@socketio.event()
def my_event(message):
    print(message['data'])
    
    socket.send_string(message['data'])

    #  Get the reply.
    ZMQmessage = socket.recv()

    emit('my_response', {'data': message['data']})

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

