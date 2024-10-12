from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import jinja2

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def do_login():
    """This is the entry point: a user sets its username and is then redirected to the new page"""
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = 'username'
        # return render_template('loggedin.html', username=username)
        return redirect(url_for('.display_username'),username=username)
    else:
        return render_template('index.html')
    
@app.route('/loggedin', methods=['GET', 'POST'])
def display_username():
    username = request.args['username']
    return render_template('loggedin.html', username=username)

    
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

if __name__ == '__main__':
    app.run()