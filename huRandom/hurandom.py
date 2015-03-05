import sqlite3

from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import csv

import pygal


app = Flask(__name__)
app.config.from_envvar('HURANDOM_SETTINGS', silent=True)


def connect_db():
    """
    Connect to a given DB defined in conf.py and exported to env vars
    """
    return sqlite3.connect(app.config['DATABASE'])
def init_db():
    """
    Initializes database. `$ python`, `>from flask import init_db`, `>init_db()`
    """
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    """
    Establish connection with database
    """
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    """
    Close connection with database
    """
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def fetch_entries():
    """
    Fetches entries from database and returns dict.
    """
    cur = g.db.execute('select text from entries order by id desc')
    entries = [dict(text=row[0]) for row in cur.fetchall()]
    return entries

@app.route('/')
def add_entry_page():
    """
    The main page where users enter number
    """
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_entry():
    """
    Adds entry to database
    """
    g.db.execute('insert into entries (text) values (?)',
                 [request.form['user_input']])
    g.db.commit()
    export_csv(fetch_entries())
    graph_data(fetch_entries())
    flash('New entry successfully added')
    return redirect(url_for('goto_data'))

@app.route('/data')
def goto_data():
    """
    Links user to data page.
    """
    nums = fetch_entries()
    return render_template('data.html', entries=nums)

@app.route('/admin')
def admin_interface():
    """
    Renders admin interface page.
    """
    return render_template('admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page for admin interface.
    """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin_interface'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """
    Logout interface.
    """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('add_entry_page'))

def export_csv(data):
    """
    Exports data into newline delimited csv file
    """
    csvfile = 'data/hurandom-raw.csv'
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in data:
            writer.writerow([val]) 

def graph_data(data):
    """
    Generates histogram of data for user
    """
    chart = pygal.Bar()
    chart.title = '`Random` Numbers'
    #chart.x_labels = map(str, range(2002, 2013))
    chart.add('Data', data)
    chart.render()
    chart.render_to_file('data/chart.svg')  
    

if __name__ == '__main__':
    app.run()
