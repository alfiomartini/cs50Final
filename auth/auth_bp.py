from flask import Blueprint, render_template, request
from flask import flash, redirect, session, url_for
from helpers import apology, login_required
from database import mydb
from werkzeug.security import check_password_hash, generate_password_hash
from view_menu import View

auth_bp = Blueprint('auth_bp', __name__, template_folder='templates',
              static_folder='static', static_url_path='/auth_static')

@auth_bp.route("/login", methods=["GET", "POST"])
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
        rows = mydb.execute("SELECT * FROM users WHERE name = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], 
                                   request.form.get("password")):
            return apology("Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # print('session[user_id]:', session['user_id'])
        # set user_id in the database
        mydb.set_userid(session['user_id'])
    
        # get view menu
        viewMenu = View()
        session['menu'] = viewMenu
        #print('session[menu]:', session['menu'])

        # Redirect user to home page
        flash('You are now logged in')
        return redirect(url_for('index'))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for('index'))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            return apology("You must provide a user name.")
        row = mydb.execute("select * from users where name = ?", (username,))
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
            mydb.execute('insert into users(name, password) values(?,?)', 
                           username, hash_passw)
            flash("You are registered.")
            return redirect(url_for('auth_bp.login'))
    else:
        return render_template('register.html')


@auth_bp.route('/change', methods=['GET', 'POST'])
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
        row = mydb.execute("select * from users where id = ?", 
              (session['user_id'],))
        oldhash = row[0]['hash']
        if not check_password_hash(oldhash, old):
            return apology('Current password is wrong.')
        newhash = generate_password_hash(new)
        # update database with new user password 
        mydb.execute('update users set hash = ? where id = ?',
                    (newhash, session['user_id'],))
        return redirect(url_for('auth_bp.logout'))
    else:
        return render_template('change.html')

