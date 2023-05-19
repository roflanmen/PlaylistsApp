from flask_socketio import SocketIO, join_room, leave_room, emit, send
from app import socketio

@socketio.on('connect', namespace='/api/chat')
def join(msg):
    print("# User Connected ...")
    join_room("chat")
    emit('message', 'Someone has entered the chat', room="chat")

@socketio.on('text', namespace='/api/chat')
def text(msg):
    print("# Message: " + msg)
    emit('message', msg, room="chat")
