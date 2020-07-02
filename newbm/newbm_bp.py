from flask import Blueprint, render_template, request
from flask import flash, redirect, session, url_for
from helpers import apology, login_required
from database import mydb
from queries import build_bookmarks
from view_menu import viewMenu


newbm_bp = Blueprint('newbm_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/newbm_static')


@newbm_bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    menu = viewMenu.catsMenu()
    categories = list(map(lambda x: {'cat_name': x['name']}, menu))
    listCats = list(map(lambda x: x['cat_name'], categories))
    if request.method == 'POST':
        # category always case independent
        category = request.form.get('category').lower()
        url = request.form.get('url')
        title = request.form.get('title')
        description = request.form.get('description')
        mydb.execute('''insert into bookmarks(categ_name, user_id, url, title, description) 
                   values(?,?,?,?,?)''',category, session['user_id'], url, title, description)
        if category not in listCats:
            mydb.execute('insert into categories(cat_name, user_id) values(?,?)', 
                    category, session['user_id'])
            mydb.execute('insert into menu(cat_name,user_id,visible) values(?,?,?)',
                    category, session['user_id'], 1)
        flash(f"Bookmark added to category {category}")
        return redirect(url_for('index'))
    else:
        #print(listCats)
        return render_template('create.html', categories=listCats, menu=menu)