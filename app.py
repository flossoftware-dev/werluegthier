from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit, disconnect
import jinja2
import uuid


app = Flask(__name__, template_folder='templates')
app.secret_key = 'development'  # Change this to a random, secret value
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
socketio = SocketIO(app, manage_session=False)

connected_users = set()
sid_to_username = {}

@app.route('/', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        if not username:
            return render_template('index.html', error="Username required")
        user_id = str(uuid.uuid4())  # Unique per browser session
        if username == 'admin':
            return redirect(url_for('display_adminpanel', username=username, user_id=user_id))
        else:
            return redirect(url_for('display_userpanel', username=username, user_id=user_id))
    return render_template('index.html')

@app.route('/loggedin/<username>/<user_id>')
def display_userpanel(username, user_id):
    if username == 'admin':
        return redirect(url_for('do_login'))
    return render_template('loggedin.html', username=username, user_id=user_id)

@app.route('/sessionmaster/<username>/<user_id>')
def display_adminpanel(username, user_id):
    if username != 'admin':
        return redirect(url_for('do_login'))
    return render_template('sessionmaster.html', username=username, user_id=user_id)

"""Admin panel: Start a new session."""
@app.route('/adminsession')
def display_adminsession():
    return render_template('adminsession.html', username='Sessionmaster', users=list(connected_users))

"""Admin panel: Start a new session."""
@app.route('/usersession')
def display_usersession(username):
    return render_template('usersession.html', username=username)


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@socketio.on('start_sessions')
def start_sessions_windows():
    emit('redirect_event', url_for('display_adminsession'), broadcast=True)

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('register_user')
def handle_register_user(data):
    user_id = data.get('user_id')
    username = data.get('username')
    if user_id and username:
        sid_to_username[request.sid] = (user_id, username)
        connected_users.add((user_id, username))
        print(f"User registered: {username}, Total users: {len(connected_users)}")
        emit('update_users', sorted([u[1] for u in connected_users]), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_info = sid_to_username.pop(request.sid, None)
    if user_info and user_info in connected_users:
        connected_users.remove(user_info)
        socketio.emit('update_users', [u[1] for u in connected_users])

@socketio.on('change_background_color')
def handle_color_change(color):
    emit('apply_background_color', color, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)