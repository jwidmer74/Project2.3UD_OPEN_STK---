from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash
import uuid
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, verify_id_token
from oauth2client.client import FlowExchangeError
import os
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from database_setup2 import Base, Category, Item


APP_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_ID = json.loads(open("client_secret.json", "r").read())[
    'web']['client_id']
print(CLIENT_ID)
app = Flask(__name__)
engine = create_engine("sqlite:///catalog.db?check_same_thread=False")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/category/<int:category_id>/menu/JSON')
def categoryMenuJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])
	
@app.route('/category/<int:category_id>/menu/<int:menu_id>/JSON')
def itemJSON(category_id, menu_id):
    Item = session.query(Item).filter_by(id=menu_id).one()
    return jsonify(Item=Item.serialize)
	
@app.route('/category/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])
	
@app.route('/categoryauth/')
def showAuthCategories():
    if "username" not in login_session:
        return redirect('/login')
    categories = session.query(Category).all()
    conn = engine.connect()
    latestItems = session.query(
        (select([Item.name]).order_by((Item.name).desc()).limit(10))).all()
    return render_template(
        'categoriesAuth.html',
        latestItems=latestItems,
        categories=categories,
        login_session=login_session)
# Show all categories

@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    conn = engine.connect()
    latestItems = session.query(
        (select([Item.name]).order_by((Item.name).desc()).limit(10))).all()
    return render_template(
        'categories.html',
        latestItems=latestItems,
        categories=categories,
        login_session=login_session)
# Create a new category

@app.route('/categoryauth/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name=request.form['name'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        return render_template('newCategory.html')
# return "This page will be for making a new category"
# Edit a category

@app.route('/categoryauth/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    if "username" not in login_session:
        return redirect('/login')
    editedCategory = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            session.add(editedCategory)
            session.commit()
            return redirect(url_for('showCategories'))
    else:
        return render_template('editCategory.html', category=editedCategory)
# return 'This page will be for editing category %s' % category_id
# Delete a category

@app.route('/categoryauth/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    if "username" not in login_session:
        return redirect('/login')
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
# Show a category menu

@app.route('/categoryauth/<int:category_id>/')
@app.route('/categoryauth/<int:category_id>/menu/')
def showMenuAuth(category_id):
    if "username" not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('menuAuth.html', items=items, category=category)
# Show a category menu
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu/')

def showMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('menu.html', items=items, category=category)
	
@app.route(
    '/categoryauth/<int:category_id>/menu/new/',
    methods=[
        'GET',
        'POST'])
def newItem(category_id):
    if "username" not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = Item(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            material=request.form['material'],
            category_id=category_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showMenuAuth', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)
    return render_template('newItem.html', category=category)
	
@app.route('/categoryauth/<int:category_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, menu_id):
    if "username" not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['material']:
            editedItem.material = request.form['material']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template(
            'editItem.html',
            category_id=category_id,
            menu_id=menu_id,
            item=editedItem)
			
@app.route('/login')
def login():
    state = uuid.uuid4()
    login_session['state'] = unicode(str(state), 'utf-8')
    return render_template('login.html', state=state)
	
@app.route('/logout')
def logout():
    print(type(login_session))
    if "username" in login_session:
        del login_session["username"]
    return render_template('logout.html')
	
@app.route('/gconnect', methods=["POST"])
def gconnect():
    print(request.args.get("state"), "==", login_session["state"])
    if(str(request.args.get("state")) != str(login_session["state"])):
        print("Invalid State")
        response = make_response(json.dumps("Invalid State parameter"), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    code = request.data
    try:
        print("code", code)
        oauth_flow = flow_from_clientsecrets(
            os.path.join(APP_PATH, "client_secret.json"), scope="")
        oauth_flow.redirect_uri = 'postmessage'
        oauth_flow.access_type = 'offline'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError as e:
        print('Authentication has failed: {}'.format(str(e)))
        response = make_response(json.dumps("Failed to upgrade"), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    print(result)
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    login_session['access_token'] = access_token
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output
# Delete a menu item

@app.route(
    '/categoryauth/<int:category_id>/menu/<int:menu_id>/delete',
    methods=[
        'GET',
        'POST'])
def deleteItem(category_id, menu_id):
    itemToDelete = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)