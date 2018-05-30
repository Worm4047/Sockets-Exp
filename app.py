from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}

def ack(msg):
    print(msg)

@app.route('/')
def index():
    return render_template('index.html',**values)

@socketio.on('connect')
def test_connect():
    print("Connected", request.sid)
    emit('after connect',  {'data':'Lets dance'}, callback=ack)

@socketio.on('value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')