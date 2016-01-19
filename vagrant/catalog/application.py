# name: Andrew Wang
# Full Stack Web Developer Nanodegree
# Project 3 Catalog

import json
import psycopg2
from flask import Flask, render_template, redirect, flash, url_for
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

import database_setup
from database_setup import User, Category, Item, session, get_categories, make_json

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
def login():
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
@app.route('/catalog')
def make_catalog():
    if 'username' not in login_session:
        #return "Hello World"
        #return redirect('/login')
        item_list = show_items()
        cat_list = show_categories()
        return render_template('catalog.html', title="Catalog",
            item_list=item_list, logged=url_for('.login'), logact="Login",
            cat_list=cat_list)
    else:
        #ret = check_create_user()
        #user_list = show_users()
        #temp_email = login_session['email']
        #logout = url_for('.gdisconnect')
        #return render_template('catalog.html', title="Catalog", 
        #    users=user_list, email=temp_email, logout_url=logout,
        #    userin=ret, logged=url_for('.gdisconnect'), logact="Logout")
        item_list = show_items()
        cat_list = show_categories()
        print item_list
        return render_template('catalog.html', title="Catalog",
            item_list=item_list, logged=url_for('.gdisconnect'), logact="Logout",
            create=url_for('.create_page'), cat_list=cat_list)


@app.route('/create')
def create_page(title="Create"):
    if 'username' not in login_session:
        return redirect('/login')
    return render_template('create.html', title=title)


@app.route('/catalog/<catname>')
def make_category(catname):
    """
    This function makes a category page
    The category page shows every item in the category
    """

    # Check if logged in to change login/logout link
    if 'username' not in login_session:
        t_logact = "Login"
        t_logged = url_for('.gdisconnect')
    else:
        t_logact = "Logout"
        t_logged = url_for('.login')

    # Get all items in category
    query = session.query(Item).join(Category).filter(Category.category_name == catname) 
    ret = [x.item_name for x in query]
    return render_template('category.html', title=catname, catlist=ret,
        logged=t_logged, logact=t_logact)


@app.route('/catalog/<catname>/<itemname>')
def make_item(catname, itemname):
    """
    This function makes the page for items
    Shows description of item
    If the user is logged in will check if user owns item
    If user owns item, will have edit and delete buttons
    """

    # Check if logged in or not
    if 'username' not in login_session:
        t_logact = "Login"
        t_logged = url_for('.login')
        query = session.query(Item).filter(Item.item_name==itemname).one()
        return render_template('item.html', title=itemname, item=itemname, 
            desc=query.description, logged=t_logged, logact=t_logact)
    else:
        t_logact = "Logout"
        t_logged = url_for('.gdisconnect')
        if owns_item(itemname):
            t_edit=True
        else:
            t_edit=False
        query = session.query(Item).filter(Item.item_name==itemname).one()
        return render_template('item.html', title=itemname, item=itemname, 
            desc=query.description, logged=t_logged, logact=t_logact,
            edit=t_edit)


# Create JSON endpoint
@app.route('/catalog.json')
def endpoint():
    return "JSON"


def owns_item(item):
    """
    This function checks if currently logged in user owns an item
    returns True if is owner
    returns False if not
    """
    query = session.query(Item).join(User).filter(User.email == login_session['email'])
    query.filter(Item.item_name==item)
    return query.count() != 0



def show_categories():
    """
    This function shows all categories
    returns a list of categories
    """
    query = session.query(Category)
    ret = [x.category_name for x in query]
    return ret
    

def show_items():
    """
    This function shows all items
    returns a list of (item,category) tuples
    """
    query = session.query(Item)
    ret = []
    for x in query:
        t_name = x.item_name
        t_cat = session.query(Category).filter(Category.id==x.cat_id).one()
        ret.append ((t_name, t_cat.category_name))
    #ret = [(x.item_name, x.category) for x in query]
    return ret


def no_email():
    """
    This function checks if email is in database
    returns True if user email in database
    returns False if not
    """
    query = session.query(User).filter(User.email == login_session['email'])
    print query.count()
    return query.count() == 0


def insert_user():
    """
    This function inserts a user into database
    """
    temp_email = login_session['email']
    temp_name = login_session['username']
    temp_pic = login_session['picture']
    temp_user = User(email=temp_email, name=temp_name, picture=temp_pic)
    session.add(temp_user)
    session.commit()


def check_create_user():
    """
    this function checks if a new user needs to be created
    first check if email in database
    if not, make new user
    """
    print "check and creating user"
    if no_email():
        print "no email"
        insert_user()
    query = session.query(User)
    print "about to return"
    return query


# UNNECESSARY FUNCTIONS ******************************************************
# Function for connecting to psycopg2 database
#def connect():
#    """
#    Returns a tuple containing database connection and a cursor
#    connection is the database connection
#    cursor is the cursor
#    retruned value: (connection, cursor)
#    """
#    temp_connect = psycopg2.connect("dbname=catalog")
#    temp_cursor = temp_connect.cursor()
#    return (temp_connect, temp_cursor)


# Function for accessing entries
#def show_users():
#    """
#    This function returns a list of a dictionary entries
#    """
#    db, cursor = connect()
#    cursor.execute('SELECT id, user_name, hash, salt FROM '
#                   'users ORDER BY id DESC')
#    entries = [dict(id=row[0], user_name=row[1],
#              hash_str=row[2], salt=row[3])
#              for row in cursor.fetchall()]
#    db.close()
#    return entries


# Accesses exactly one thing
#def show_items():
#    """
#    This function shows only those items that
#    where created by the user
#    """
#    db, cursor = connect()
#    cursor.execute()
#    entries = [('SELECT * FROM users')
#              for row in cursor.fetchall()]
#    db.close()
#    print entries
#    return entries


# hashes a password
# returns a tuple containing the hash and salt
#def hash_password(pword):
#    salt = b64encode(urandom(8))
#    salted_hash = salt + b64encode(pword)
#    m = hashlib.sha256()
#    m.update(salted_hash)
#    return (m.hexdigest(), salt)


#def check_password(pword, hashed, salt):
#    temp_pword = salt + b64encode(pword)
#    m = hashlib.sha256()
#    m.update(temp_pword)
#    new_hash = m.hexdigest()
#    return new_hash == hashed
# End unnecessary functions *********************************************


if __name__ == '__main__':
    #for instance in session.query(Category):
    #    print instance

    #for instance in session.query(User):
    #    print instance

    #for instance in session.query(Item):
    #    print instance

    #a,b = get_categories()
    #print a,b
    #make_json()

    #with app.test_request_context():
    #    print url_for('.create_page')

    #for n in show_items():
    #    print n

    #no_email()
    app.secret_key = 'supersecretkey' # for using session
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
