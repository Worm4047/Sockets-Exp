from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

active_users = []
messages = {}
user_sid = {}


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('new user')
def new_user(message):
	# print 'Inside new user'
	user = message['username']
	sid = request.sid
	# print user, sid
	if not user in active_users:
		active_users.append(user)
		messages[user] = {}
	user_sid[user] = sid
	emit('active users updated', active_users, broadcast=True)

@socketio.on('fetch chat')
def fetch_chat(data):
	# print 'Inside fetch chat'
	username = data['username']
	userid = data['userid']
	# print username, userid, messages
	sid1 = user_sid[username]
	sid2 = user_sid[userid]
	# print sid1, sid2
	msg = []
	if messages[username] and messages[username].has_key(userid):
		msg = messages[username][userid]
	emit('display chat', msg, broadcast=False, json=True)

@socketio.on('new message')
def new_message(data):
	# print data
	message = data['message']
	username = data['from']
	chatting_with = data['to']
	msg1_dict = {"message": message, "sender": username}
	msg2_dict = {"message": message, "sender": username}
	if not messages[username].has_key(chatting_with):
		messages[username][chatting_with] = []

	if not messages[chatting_with].has_key(username):
		messages[chatting_with][username] = []
	messages[username][chatting_with].append(msg1_dict)
	messages[chatting_with][username].append(msg2_dict)
	emit('incoming message', {'message' :message, 'from':username}, room = user_sid[chatting_with]);	

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)