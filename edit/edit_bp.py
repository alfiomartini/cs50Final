from flask import Blueprint, render_template, request
from flask import flash, redirect, session
from helpers import login_required
from database import mydb

edit_bp = Blueprint('edit_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/edit_static')

@edit_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    categories = mydb.select_cats()
    bookmarks = mydb.build_bookmarks(categories)
    #print(bookmarks)
    flash('Select the bookmark you want to edit')
    return render_template('edit.html', bookmarks=bookmarks)

@edit_bp.route('/edit_id/<string:id>', methods=['GET'])
@login_required
def edit_id(id):
    bid = int(id)
    rows = mydb.execute('select * from bookmarks where id = ? and user_id = ?',
                      bid, session['user_id'])
    #print(rows[0])
    categories =  mydb.select_cats()
    listCats = list(map(lambda x: x['cat_name'], categories))
    html =  render_template('edit_id.html', row=rows[0], 
                               categories=listCats)
    #print(html)
    return html

@edit_bp.route('/apply', methods=['POST'])
# have to check if this is a new category or not
def apply():
    if request.method == 'POST':
        # categories always case independent
        category = request.form.get('category').lower() 
        title = request.form.get('title')
        url = request.form.get('url')
        description = request.form.get('description')
        bookmark_id = int(request.form.get('bid'))
        # Have to test if the categories changed? Not
        # But if it is a new category, then I have to update categories
        categories = mydb.select_cats()
        listCats = list(map(lambda x: x['cat_name'], categories))
        if category not in listCats:
           mydb.execute('insert into categories(cat_name, user_id) values(?,?)', 
                         category, session['user_id'])
        mydb.execute('''update bookmarks set categ_name = ?, user_id = ?, 
                      title = ?, url = ?, description = ? where id = ? ''',
                      category, session['user_id'], title, url, 
                      description, bookmark_id)
        flash(f'Bookmark with Title: {title} edited.')
        return redirect('/')