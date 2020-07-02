from flask import Blueprint, render_template, request
from flask import flash, redirect, session, jsonify
from helpers import apology, login_required
from database import mydb
from queries import build_search

utils_bp = Blueprint('utils_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/utils_static')

@utils_bp.route('/search/<string:term_list>', methods=['GET'])
@login_required
def search(term_list):
    term_list = term_list.lower()
    term_list = "%" + term_list + "%" 
    bookmarks = build_search(mydb, term_list)
    if bookmarks:
        html = render_template('search.html', bookmarks=bookmarks[0])
        # print(html)
        return html
    else:
        return ""

@utils_bp.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    name = request.args.get('username')
    # query database to see if there are any row with this username
    row = mydb.execute("select * from users where name = ?", (name,))
    # print('register row', row)
    if len(row) == 0:
        avail = True
    else:
        avail = False
    return jsonify(avail)