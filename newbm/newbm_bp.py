from flask import Blueprint, render_template, request
from flask import flash, redirect, session, url_for
from helpers import apology, login_required, urlImage
from helpers import processFolder, processURL
from database import mydb
from queries import build_bookmarks
from view_menu import viewMenu
import json

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
        if category not in listCats:
            mydb.execute('insert into categories(cat_name, user_id) values(?,?)', 
                    category, session['user_id'])
            mydb.execute('insert into menu(cat_name,user_id,visible) values(?,?,?)',
                    category, session['user_id'], 1)
        mydb.execute('''insert into bookmarks(categ_name, user_id, url, title, description) 
                   values(?,?,?,?,?)''',category, session['user_id'], url, title, description)
        urlImage(mydb, url)
        flash(f"Bookmark added to category {category}")
        return redirect(url_for('index'))
    else:
        #print(listCats)
        return render_template('create.html', categories=listCats, menu=menu)

@newbm_bp.route('/import_bms', methods=["GET", "POST"])
@login_required
def import_bms():
    menu = viewMenu.catsMenu()
    known_cats = mydb.execute('select cat_name from categories where user_id = ?', (session['user_id'],))
    listCats = list(map(lambda x: x['cat_name'],known_cats))
    if request.method == 'POST':
        categories = []
        urls = mydb.execute('select url from bookmarks where user_id = ?', (session['user_id'],))
        listUrls = list(map(lambda x: x['url'], urls))
        # see: https://www.kite.com/python/docs/werkzeug.FileStorage#:~:text=The%20%3Aclass%3A%60FileStorage%60%20class,the%20long%20form%20%60%60storage.
        try:
            file = request.files['filename']
        except:
            return apology('Sorry, could not open the file')
        else:
            try: 
                file_content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                return apology('Sorry, this does not seem to be a text file.')
            else:
                # json -> python dictionary
                try: 
                    bm_dict = json.loads(file_content)
                except:
                    return apology('Sorry, could not recognize this as a JSON file.')
                else:
                    # consider only bookmarks bar
                    # in the application, test if the if the key ['root']['bookmar_bar'] is defined!
                    try: 
                        bm_dict = bm_dict['roots']['bookmark_bar']['children']
                    except:
                        return apology('Sorry, could not find bookmark_bar inside the file.')
                    else:
                        for child in bm_dict:
                            if child['type'] == 'url':
                                categories.append(processURL(child))
                            if child['type'] == 'folder':
                                categories += processFolder(child)
                        for category in categories:
                            print('category', category['category'].lower())
                            print('ListCats', listCats)
                            if category['category'].lower() not in listCats:
                                mydb.execute('insert into categories(cat_name, user_id) values(?,?)', 
                                        category['category'].lower(), session['user_id'])
                                mydb.execute('insert into menu(cat_name,user_id,visible) values(?,?,?)',
                                        category['category'].lower(), session['user_id'], 1)
                                listCats.append(category['category'].lower())
                            if category['url'] in listUrls:
                                # print('updating bookmarks in import')
                                mydb.execute('''update bookmarks set categ_name=?, 
                                     title = ?, description = ? 
                                     where user_id = ? and url = ?''', 
                                      category['category'].lower(), category['title'], category['description'],
                                      session['user_id'], category['url'])
                            else:
                                mydb.execute('''insert into bookmarks(categ_name, user_id, url, title, description) 
                                        values(?,?,?,?,?)''',
                                        category['category'].lower(), session['user_id'], 
                                        category['url'], category['title'], category['description'])
                        return redirect(url_for('index'))
    else:
        return render_template('import.html', categories=listCats, menu=menu)


