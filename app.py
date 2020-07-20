from flask_mysqldb import MySQL
from flask import Flask, render_template, request,flash, redirect, url_for, session, Response
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from functools import wraps
from flask_session import Session
import os

app = Flask("__name__")
app.config['SECRET_KEY'] = os.urandom(24)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "wp_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
app.config["SESSION_TYPE"] = "filesystem"
# app.config["SESSION_USE_SIGNER"] = True

Session(app)

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


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        query = cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if query == 1:
            user = cursor.fetchone()
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı bulunamadı ya da parola hatalı', category='warning')

    return render_template("login.html")

@app.route("/")
@check_login
def index():
    return render_template("index.html")


@app.route("/logout")
def logout():
    session.pop('username')
    return redirect(url_for('login'))
    

@check_login
@socketio.on('connected')
def connected():
    emit('connected', "{} joined".format(session['username']), broadcast=True, include_self=False)

@check_login
@socketio.on('sendMessage')
def handle_message(data):
    message = data['message']
    room = data['room_name']
    emit('my response', ("{}".format(message)), broadcast=True)

@check_login
@socketio.on('logout')
def logout(data):
    session.pop('username')

@check_login
@socketio.on('typing')
def handle_typing():
    emit('typing', ("{} is typing".format(session['username'])), broadcast=True, include_self=False)

@check_login
@socketio.on('notyping')
def handle_notyping():
    emit('notyping', (''), broadcast=True, include_self=False)

@socketio.on('send')
def handle_send(msg):
    emit('send', {'username':session['username'], 'msg':msg},  broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app)