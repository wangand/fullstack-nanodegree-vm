# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog


import psycopg2
from flask import Flask, render_template
import hashlib
from os import urandom
from base64 import b64encode, b64decode
app = Flask(__name__)


# Create the index page
@app.route('/')
@app.route('/hello')
def HelloWorld():
    return render_template('catalog.html', title="cats")



# Function for connecting to psycopg2 database
def connect():
     """
     Returns a tuple containing database connection and a cursor
     connection is the database connection
     cursor is the cursor
     retruned value: (connection, cursor)
     """
     temp_connect = psycopg2.connect("dbname=catalog")
     temp_cursor = temp_connect.cursor()
     return (temp_connect, temp_cursor)


# Function for accessing entries
def show_entries():
    db, cursor = connect()
    cursor.execute('SELECT TITLE, text FROM '
                   'entries ORDER BY id DESC')
    entries = [dict(title=row[0], text=row[1]) for row in cursor.fetchall()]
    db.close()
    print entries


# hashes a password
# returns a tuple containing the hash and salt
def hash_password(pword):
    salt = b64encode(urandom(8))
    salted_hash = salt + b64encode(pword)
    m = hashlib.sha256()
    m.update(salted_hash)
    return (m.hexdigest(), salt)


def check_password(pword, hashed, salt):
    temp_pword = salt + b64encode(pword)
    m = hashlib.sha256()
    m.update(temp_pword)
    new_hash = m.hexdigest()
    return new_hash == hashed


if __name__ == '__main__':
    myHash, salt = hash_password("cat")
    print check_password("cat", myHash, salt)
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
