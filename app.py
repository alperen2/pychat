from flask_mysqldb import MySQL
from flask import Flask, render_template, request,flash, redirect, url_for, session, request, Response
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '*\x9c\xd8J\x81\x11x\xf0c\xfa\xfc\xde:\xef\x03x'
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "wp_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
socketio = SocketIO(app)
mysql = MySQL(app)



# kullanıcı giriş decarator
def check_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

    
@app.route("/")
def index():
    return render_template("index.html")


@socketio.on('join')
def handle_join(username):  
    session['username'] = username
    emit('joined', "{} joined".format(username), broadcast=True, include_self=False)
   
@socketio.on('sendMessage')
def handle_message(data):
    print(data)
    message = data['message']
    room = data['room_name']
    emit('my response', ("{}".format(message)), broadcast=True)

@socketio.on('typing')
def handle_typing():
    emit('typing', ("{} is typing".format(session['username'])), broadcast=True, include_self=False)

@socketio.on('notyping')
def handle_notyping():
    emit('notyping', (''), broadcast=True, include_self=False)

@socketio.on('send')
def handle_send(msg):
    emit('send', {'username':session['username'], 'msg':msg},  broadcast=True, include_self=False)


@socketio.on('video')
def handle_video(data):
    print(data)
    print(1)
    emit('video', data,  broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app)