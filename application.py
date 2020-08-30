import os
# import redis
from flask import Flask, render_template, session
from flask import url_for, redirect
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
 
from helpers import login_required, apology
from database import mydb
from queries import build_bookmarks
# from view_menu import catsMenu
from view_menu import viewMenu

from auth.auth_bp import auth_bp
from edit.edit_bp import edit_bp
from remove.remove_bp import remove_bp
from utils.utils_bp import utils_bp
from newbm.newbm_bp import newbm_bp

# Configure application
app = Flask(__name__)
  
# app.secret_key = os.getenv("SESSION_KEY")

app.register_blueprint(auth_bp)
app.register_blueprint(edit_bp)
app.register_blueprint(remove_bp)
app.register_blueprint(utils_bp)
app.register_blueprint(newbm_bp)


# Ensure templates are auto-reloaded
# Whether to check for modifications of the template source and reload it automatically.
# By default the value is None which means that Flask checks original file only in debug mode.
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
# see https://roadmap.sh/guides/http-caching
# see https://pythonise.com/series/learning-flask/python-before-after-request
@app.after_request
def after_request(response):
    # Cache-Control specifies how long and in what manner should the content be cached. 
    # no-store specifies that the content is not to be cached by any of the caches
    # (public, private, server)
    # must-revalidate avoids that. If this directive is present, it means that stale content 
    # cannot be served in any case and the data must be re-validated from the server before serving.
    # no-cache indicates that the cache can be maintained but the cached content is to be re-validated 
    # (using ETag for example) from the server before being served. 
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # how long a cache content should be considered fresh? never.
    response.headers["Expires"] = 0
    return response

 

# Configure session to use local filesystem (instead of signed cookies)
# mkdtemp() creates a temporary directory in the most secure manner possible. 
# There are no race conditions in the directory’s creation. The directory is 
# readable, writable, and searchable only by the creating user ID.
# The user of mkdtemp() is responsible for deleting the temporary directory and its 
# contents when done with it.

# app.config["SESSION_FILE_DIR"] = mkdtemp()
# session is cleared after exiting the browser
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# see: https://stackoverflow.com/questions/57691525/redirects-not-working-properly-on-heroku-but-they-do-on-localhost

@app.route("/")
@login_required
def index():
    menu = viewMenu.catsMenu()
    categories = list(map(lambda x: {'cat_name': x['name']}, menu))
    bookmarks = build_bookmarks(mydb, categories)
    # print(bookmarks)
    return render_template('index.html', bookmarks=bookmarks, menu=menu)

@app.route('/view_mode', methods=['GET'])
@login_required
def view_mode():
    if session['list_view']:
        session['list_view'] = False 
        session['grid_view'] = True
    else:
        session['list_view'] = True
        session['grid_view'] = False
    return redirect(url_for('index'))

@app.route('/view/<string:cat_name>', methods=['GET'])
@login_required
def view(cat_name):
    truthy = viewMenu.getItemStatus(cat_name)
    print(session['user_id'])
    print('truty:', truthy)
    if truthy:
        viewMenu.setChecked(cat_name, False)
    else:
        viewMenu.setChecked(cat_name, True)
    return redirect(url_for('index'))

@app.route('/view_all', methods=['GET'])
@login_required
def view_all():
    menu = viewMenu.catsMenu()
    categories = list(map(lambda x: {'cat_name': x['name']}, menu))
    for cat in categories:
        viewMenu.setChecked(cat['cat_name'], True)
    return redirect(url_for('index'))

@app.route('/hide_all', methods=['GET'])
@login_required
def hide_all():
    menu = viewMenu.catsMenu()
    categories = list(map(lambda x: {'cat_name': x['name']}, menu))
    for cat in categories:
        viewMenu.setChecked(cat['cat_name'], False)
    return redirect(url_for('index'))
 
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run()
    #app.run()
