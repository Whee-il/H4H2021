from flask import Flask, render_template
from flask_socketio import SocketIO, emit
#import socket

#Flask Crap
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/', defaults={"instruction": "Go"})
@app.route('/<instruction>')
def index(instruction):
    return render_template('index.html', instruction=instruction)

@socketio.event()
def my_event(message):
    print(message['data'])
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

