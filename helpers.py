import os
import requests
import urllib.parse

from flask import url_for
from flask import redirect, render_template, request, session
from functools import wraps


def shorten_title(name, size):
    # using slice notation [:]
    short = name.lower().title()[0:size]
    if len(name) > size:
        short += '...'
    return short

def apology(message):
    return render_template("apology.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.
    https://www.datacamp.com/community/tutorials/decorators-python
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # We use session.get("user_id") to check if the key exists in the session.
        if session.get("user_id") is None:
            return redirect(url_for('auth_bp.login'))
        return f(*args, **kwargs)
    return wrapper
