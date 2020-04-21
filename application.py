import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, shorten_title

# Configure application
app = Flask(__name__)

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
    response.headers["Cache-Control"] = "no-cache"
    # how long a cache content should be considered fresh? never.
    response.headers["Expires"] = 0
    return response

 

# Configure session to use local filesystem (instead of signed cookies)
# mkdtemp() creates a temporary directory in the most secure manner possible. 
# There are no race conditions in the directory’s creation. The directory is 
# readable, writable, and searchable only by the creating user ID.
# The user of mkdtemp() is responsible for deleting the temporary directory and its 
# contents when done with it.

app.config["SESSION_FILE_DIR"] = mkdtemp()
# session is cleared after exiting the browser
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/cs50final.db")

# enables foreign key constraints at runtime
#db.execute('PRAGMA foreign_keys = ON')

 
@app.route("/")
@login_required
def index():
    rows = db.execute('''select url, title, description from resources
                         where user_id = ?''', (session['user_id'],))
    for row in rows:
        row['short_title'] = shorten_title(row['title'])
        row['tooltip'] = row['title'] + '\n' + row['url']
    #print(rows)
    return render_template('index.html', rows=rows)

@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    if request.method == 'POST':
        url = request.form.get('url')
        title = request.form.get('title')
        description = request.form.get('description')
        db.execute('insert into resources(user_id, url, title, description) values(?,?,?,?)', 
                           session['user_id'], url, title, description)
        return redirect('/')
    else:
        return render_template('create.html')
  
@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    name = request.args.get('username')
    if len(name) < 1:
        return jsonify(False)
    # query database to see if there are any row with this username
    row = db.execute("select * from users where username = ?", (name,))
    if len(row) == 0:
        avail = True
    else:
        avail = False
    return jsonify(avail)

 
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("You must provide a username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("You must provide a password.")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE name = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], 
                                   request.form.get("password")):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return apology("You must provide a user name.")
        row = db.execute("select * from users where name = ?", (username,))
        if len(row) == 1:
            return apology('This user is already registered.')
         # just to make it sure. It could never happen
        elif len(row) > 1:
            return apology('Duplicates in the database') 
        password = request.form.get('password')
        if not password:
            return apology("You must provide a passord")
        confirmation = request.form.get('confirmation')
        if not confirmation:
            return apology("You must confirm your passord.")
        hash_passw = generate_password_hash(password)
        if not check_password_hash(hash_passw, confirmation):
            return apology('Passwords do not match.')
        else:
            db.execute('insert into users(name, password) values(?,?)', 
                           username, hash_passw)
            flash("You are registered.")
            return render_template('registered.html')
    else:
        return render_template('register.html')


@app.route('/change', methods=['GET', 'POST'])
@login_required
def change():
    if request.method == 'POST':
        # access post parameters
        old = request.form.get('oldpassword')
        new = request.form.get('newpassword')
        conf = request.form.get('confirmation')
        # see if new and confirmation password match
        if new != conf:
            return apology("New passord and confirmation don't match.")
        # query database to access user data
        row = db.execute("select * from users where id = ?", 
              (session['user_id'],))
        oldhash = row[0]['hash']
        if not check_password_hash(oldhash, old):
            return apology('Current password is wrong.')
        newhash = generate_password_hash(new)
        # update database with new user password 
        db.execute('update users set hash = ? where id = ?',
                    (newhash, session['user_id'],))
        return redirect('/logout')
    else:
        return render_template('change.html')


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == '__main__':
    app.run(debug=True)
