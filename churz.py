import os
import sys
import signal
import base64
import shelve
from bottle import get, post, run, redirect, request, abort


base_url = 'http://s.dbrgn.ch/'
db = shelve.open('data.db')


@get('/')
@get('/<path:re:[a-zA-Z0-9_\-]+>')
def retrieve(path=None):
    """Redirect to real URL."""
    if path is None:
        return '<img src="http://i1.kym-cdn.com/photos/images/newsfeed/000/345/309/5eb.gif">'
    try:
        redirect(db[path])
    except KeyError as e:
        abort(404, 'URL %s not found.' % e.message)


@post('/')
def store():
    """Shorten new URL."""
    url = request.POST.get('url')
    while 1:
        rand_bytes = os.urandom(3)
        rand_string = base64.urlsafe_b64encode(rand_bytes)
        if not rand_string in db:
            db[rand_string] = url
            break
    return base_url + rand_string


def sigint(signal, frame):
    """Handle SIGINT signal to properly close shelve."""
    db.close()
    sys.exit()
signal.signal(signal.SIGINT, sigint)


run(host='localhost', port=8080)
