# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog


import psycopg2
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)


# Create the index page
#@app.route('/')
#@app.route('/hello')
#def HelloWorld():
#    return "<h1>Hello World</h1>"



# Function for connecting to psycopg2 database
def connect():
   """
   Returns a tuple containing database connection and a cursor
   connection is the database connection
   cursor is the cursor
   retruned value: (connection, cursor)
   """
   temp_connect = psycopg2.connect("dbname=flaskr")
   temp_cursor = temp_connect.cursor()
   return (temp_connect, temp_cursor)


# Function for accessing entries route to app
@app.route('/')
def show_entries():
    db, cursor = connect()
    cursor.execute('SELECT TITLE, text FROM '
    	           'entries ORDER BY id DESC')
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    db.close()
    print entries
    return render_template('show_entries.html', entries = entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db, cursor = connect()
    tempTitle = request.form['title']
    tempText = request.form['text']
    cursor.execute('insert into entries (title, text) values (%s, %s)',
                 (tempTitle, tempText))
    db.commit()
    db.close()
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
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#show_entries()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
