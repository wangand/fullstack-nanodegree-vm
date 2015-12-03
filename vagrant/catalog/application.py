# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog

import json
import psycopg2
from flask import Flask, render_template, redirect, flash
#from flask.ext.login import LoginManager
import hashlib
from os import urandom
from base64 import b64encode, b64decode
from flask import session as login_session
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from flask import make_response
import requests
from flask import request
import httplib2

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Item Catalog Application"

@app.route('/gconnect', methods=['POST'])
def gconnect():
    print "start"
    print request.args.get('state')
    print login_session['state']
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    print "state token validated"

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print "Credentials object upgraded"

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
    print "Access token is valid"

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print "Access token is used for the intended user"

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    print "access tokein is valid for this app"

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    print "store access token"

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    print "user info get"

    data = answer.json()
    print "data = answer.json()"

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: '
    output += '150px;-webkit-border-radius: '
    output += '150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.
        digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=login_session['state'])


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: ' 
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token'] 
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Create the index page
@app.route('/')
@app.route('/hello')
def HelloWorld():
    if 'username' not in login_session:
        return redirect('/login')
    user_list = show_users()
    return render_template('catalog.html', title="cats", users=user_list)


# Create JSON endpoint
@app.route('/catalog.json')
def endpoint():
    return "JSON"
    


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
def show_users():
    """
    This function returns a list of a dictionary entries
    """
    db, cursor = connect()
    cursor.execute('SELECT id, user_name, hash, salt FROM '
                   'users ORDER BY id DESC')
    entries = [dict(id=row[0], user_name=row[1],
              hash_str=row[2], salt=row[3])
              for row in cursor.fetchall()]
    db.close()
    return entries


# Accesses exactly one thing
def show_items():
    """
    This function shows only those items that
    where created by the user
    """
    db, cursor = connect()
    cursor.execute()
    entries = [('SELECT * FROM users')
              for row in cursor.fetchall()]
    db.close()
    print entries
    return entries


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
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
