import os
import requests
import urllib.parse
from PIL import Image
from io import BytesIO
from urllib.parse import urlparse

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

def getImage(img_url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
        resp = requests.get(img_url, headers=headers)
        image = Image.open(BytesIO(resp.content))
    except:
        image = None 

    return image

def getImageLink(url):
  
    # Contact API
    try:
        api_key = os.environ.get("LINK_PREVIEW_KEY")
        URL = f"http://api.linkpreview.net/?key={api_key}&q={url}"
        json_resp = requests.get(URL)
        json_resp.raise_for_status()
    except requests.RequestException:
        return None
    else:
        # response is in json notation. json() is a json decoder, i.e,
        # maps json back to object format
        # see https://requests.readthedocs.io/en/master/user/quickstart/
        img_preview = json_resp.json()
        img_url = img_preview['image']
        return img_url

def saveImage(img_url):
    image = getImage(img_url)
    if image:
        url_obj = urlparse(img_url)
        img_name = url_obj.netloc + url_obj.path
        img_name = img_name.replace("/", "_")  
        img_name = img_name.replace('*', '_')
        image.save(f'static/preview/{img_name}') 
        return img_name
    else:
        img_name = None
    return img_name

def urlImage(db, url):
    img_url = getImageLink(url)
    if img_url:
        img_name = saveImage(img_url)
        if img_name:
            entry = db.execute('select url, image from images where url = ?', (url,))
            if len(entry) == 0:
                db.execute('insert into images(url, image) values(?,?)', (url, img_name))
            else:
                # if url != entry[0]['url']:
                db.execute('update images set url = ?, image = ? where url = ?', (url, img_name,url))
        else:
            # print('else saveImage')
            img_name = 'bm-small.png' #default_image 
            db.execute('insert into images(url, image) values(?,?)', (url, img_name))
    else: 
        # print('else getImageLink')
        img_name = 'bm-small.png' #default_image 
        db.execute('insert into images(url, image) values(?,?)', (url, img_name))

def processURL(dict):
    bm = {}
    bm['category'] = 'Universal'
    bm['title'] = dict['name']
    bm['url'] = dict['url']
    return bm

def processFolder(folder):
    category = folder['name']
    bookmarks = []
    for bm_child in folder['children']:
        bm={}
        bm['category'] = category
        bm['title'] = bm_child['name']
        bm['url'] = bm_child['url']
        bookmarks.append(bm)
    return bookmarks

