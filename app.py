from socket import SocketIO, socket
from webbrowser import get
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO, join_room, leave_room, emit
from flask_session import Session

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret"
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

socketio = SocketIO(app, manage_session=False)

users = {}

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/chat', methods=["GET", "POST"])
def chat():
    if (request.method=="POST"):
        username = request.form['username']
        if (username != ""):
            room = 'room'
            session['username'] = username

            session['room'] = room
            return render_template('chat.html', session = session)
        else :
            flash("User name can not be empty!")
            return render_template('index.html')
    else:
        if (session.get('username') is not None):
            return render_template('chat.html', session = session)
        else:
            return redirect(url_for('index'))


@socketio.on('join', namespace='/chat')
def join(message):
    room = session.get('room')
    join_room(room)
    emit('user-connected', {'msg': session.get('username') + ' has joined the chat.'}, room = room)

@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('username') + ': ' + message['msg'] }, room = room)

@socketio.on('disconnect', namespace='/chat')
def clear_user():
    room = session.get('room')
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('user-disconnected', {'msg: username ' + 'has left the room.'}, room=room)




if __name__ == '__main__':
    socketio.run(app)