from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}

@app.route('/')
def index():
    return render_template('index.html',**values)

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('Slider value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')