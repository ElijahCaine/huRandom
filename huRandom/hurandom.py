import sqlite3

from contextlib import closing

import os

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('HURANDOM_SETTINGS', silent=True)


def connect_db():
    """
    Connects to the specified database.
    """
    return sqlite3.connect(app.config['DATABASE'])


@app.cli.command('initdb')
def initdb_command():
    """
    Creates the database tables.
    """
    init_db()
    print('Initialized the database.')

def init_db():
    """
    Initializes the database.
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    """
    Make sure we are connected to the database each request.
    """
    g.db = connect_db()

@app.after_request
def after_request(response):
    """
    Closes the database again at the end of the request.
    """
    g.db.close()
    return response

@app.route('/')
def show_entries():
    cur = g.db.execute('select text from entries order by id desc')
    entries = [dict(text=row[0]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (text) values (?)',
                 [request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('templates/login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


# Starts application.
if __name__ == '__main__':
    app.run()

