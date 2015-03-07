from os import environ

import sys

import sqlite3

from contextlib import closing

from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import csv

import pygal
from pygal.style import CleanStyle

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
    entries = [check_num(rows[0]) for rows in cur.fetchall()] 
    entries.sort()
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
    try:
        float(request.form['user_input'])
    except:
        new = None
        flash('\'' + request.form['user_input'] + '\' isn\'t a real number!')
        return redirect(url_for('add_entry_page'))

    g.db.execute('insert into entries (text) values (?)',
                 [request.form['user_input']])
    g.db.commit()
    export_csv()
    flash('\'' + request.form['user_input'] + '\' successfully added.')
    return redirect(url_for('goto_data'))

@app.route('/data')
def goto_data():
    """
    Links user to data page.
    """
    n = fetch_entries()
    compile_data(n)
    chart = graph_data(n)
    return render_template('data.html', entries=n, chart=chart)

@app.route('/admin')
def admin_page():
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
            return redirect(url_for('admin_page'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """
    Logout interface.
    """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('add_entry_page'))

def export_csv():
    """
    Exports data into newline delimited csv file.
    """
    file_path = 'huRandom/static/hr_raw.csv'
    with open(file_path, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        for val in fetch_entries():
            writer.writerow([val]) 

def check_num(val):
    """
    Checks if input is float or integer
    returns approprately typed value
    """
    try:
        if float(val) == round(float(val)):
            return int(val)
        elif float(val) != round(float(val)):
            return float(val)
    except:
        return None

def graph_data(data):
    """
    Generates histogram of data for user
    """
    graph_data, axis = compile_data(data)
    chart = pygal.Bar(fill=True,
                      interpolate='cubic',
                      style=CleanStyle,
                      no_data_text='Not enough data to science :(',
                      title_font_size=30,
                      show_legend=False,
                      x_title='Range',
                      y_title='Frequency',
                      label_font_size=12.5,
                      x_label_rotation=30,
                      title="'Random' Numbers",
                      x_labels=axis,
                      no_data_font_size=30)
    chart.add('Data', graph_data)
    chart.render()
    return chart.render(is_unicode=True)

def compile_data(data):
    bin_num = 10

    print(data)

    if len(data) > bin_num:
        output = [0 for i in range(bin_num)]
        axis = ['-' for i in range(bin_num)]
        bin_range = int((max(data) - min(data))/bin_num)+1
        j_old = 0

        print(bin_range)
        for i in range(bin_num):
            axis[i] = str((bin_range*i)+min(data))
            print(i)
            for j in range(j_old, len(data)):
                print(j)
                if (bin_range*i)+min(data) < data[j] and data[j] <= (bin_range*(i+1)+min(data)):
                    output[i] += 1
                else:
                    j_old = j
                    break
            axis[i] += ("-" +  str(bin_range*(i+1)+min(data)))
        print(output)
        return (output, axis)
    axis = ['-' for i in range(len(data))]
    return (data, axis)

@app.route('/about')
def about_page():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host=environ.get('APP_IP'))
