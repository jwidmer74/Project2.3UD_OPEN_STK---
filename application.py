from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from database_setup2 import Base, Category, Item

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Fake categories
# category = {'name': 'The CRUDdy Crab', 'id': '1'}





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
    categories = session.query(Category).all()
    conn = engine.connect()
    
    #latestItems = conn.execute(select([Item.name])).scalar()
    latestItems = session.query((select([Item.name]).order_by((Item.name).desc()).limit(10))).all()
    return render_template('categoriesauth.html',latestItems=latestItems,categories=categories)	

# Show all categories
@app.route('/')
@app.route('/category/')
def showCategories():
    categories = session.query(Category).all()
    conn = engine.connect()
    
    #latestItems = conn.execute(select([Item.name])).scalar()
    latestItems = session.query((select([Item.name]).order_by((Item.name).desc()).limit(10))).all()
    return render_template('categories.html',latestItems=latestItems,categories=categories)

# Create a new category
@app.route('/category/new/', methods=['GET', 'POST'])
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


@app.route('/category/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
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


@app.route('/category/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        session.delete(categoryToDelete)
        session.commit()
        return redirect(
            url_for('showCategories', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=categoryToDelete)
    # return 'This page will be for deleting category %s' % category_id

# Show a category menu
@app.route('/categoryauth/<int:category_id>/')
@app.route('/categoryauth/<int:category_id>/menu/')
def showMenuAuth(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('menuAuth.html', items=items, category=category)
    # return 'This page is the menu for category %s' % category_id

# Show a category menu
@app.route('/category/<int:category_id>/')
@app.route('/category/<int:category_id>/menu/')
def showMenu(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template('menu.html', items=items, category=category)
    # return 'This page is the menu for category %s' % category_id

	# Create a new menu item

@app.route('/categoryauth/<int:category_id>/menu/new/', methods=['GET', 'POST'])
def newItem(category_id):
    if request.method == 'POST':
        newItem = Item(name=request.form['name'], description=request.form['description'], price=request.form['price'], material=request.form['material'], category_id=category_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenuAuth', category_id=category_id))
    else:
        return render_template('newItem.html', category_id=category_id)

    return render_template('newItem.html', category=category)
    # return 'This page is for making a new menu item for category %s'
    # %category_id

	# Edit a menu item


@app.route('/categoryauth/<int:category_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editItem(category_id, menu_id):
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

        return render_template('editItem.html', category_id=category_id, menu_id=menu_id, item=editedItem)

# return 'This page is for editing menu item %s' % menu_id

# Delete a menu item


@app.route('/categoryauth/<int:category_id>/menu/<int:menu_id>/delete',methods=['GET', 'POST'])
def deleteItem(category_id, menu_id):
    itemToDelete = session.query(Item).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', category_id=category_id))
    else:
        return render_template('deleteItem.html', item=itemToDelete)
		# return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
