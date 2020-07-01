from flask import Blueprint, render_template, request
from flask import flash, redirect, session, url_for
from helpers import login_required
from database import mydb
 

remove_bp = Blueprint('remove_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/remove_static')

@remove_bp.route('/rem_cat', methods=['GET'])
@login_required
def rem_cat():
    categories =  mydb.select_cats()
    listCats = list(map(lambda x: x['cat_name'], categories))
    flash('Warning: Removing a category implies deleting all bookmarks linked to it')
    return render_template('rem_cat.html', categories=listCats)

@remove_bp.route('/rem_cat_name', methods=['POST'])
@login_required
def rem_cat_name():
    categories =  mydb.select_cats()
    listCats = list(map(lambda x: x['cat_name'], categories))
    if request.method == 'POST':
        name = request.form.get('category')
        if name in listCats:
            mydb.execute('delete from bookmarks where categ_name = ? and user_id = ?', 
                    (name, session['user_id']))
            mydb.execute('delete from categories where cat_name = ? and user_id = ?', 
                    (name, session['user_id']))
            flash(f'Category: {name} and all its posts removed')
            return redirect(url_for('index'))
        else:
            flash(f'Category: {name} is unknown')
            return redirect(url_for('index'))

    

@remove_bp.route('/rem_bookmark', methods=['GET','POST'])
@login_required
def rem_bookmark():
    categories = mydb.select_cats()
    bookmarks = mydb.build_bookmarks(categories)
    #print(bookmarks)
    flash('Select the bookmark you want to remove')
    return render_template('rem_bookmark.html', bookmarks=bookmarks)



@remove_bp.route('/rem_book_id/<string:id>', methods=['GET'])
@login_required
def rem_book_id(id):
    bid = int(id)
    rows = mydb.execute('select * from bookmarks where id = ? and user_id = ?',
                      bid, session['user_id'])
    title = rows[0]['title']
    mydb.execute('delete from bookmarks where id = ?', (bid,))
    flash(f'Bookmark with Title: {title} removed.')
    # update session['menu']
    # viewMenu = View()
    # session['menu'] = viewMenu
    return (url_for('index'))
