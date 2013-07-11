"""Churz. Yet another simple URL shortener.

Usage:
    churz.py [-p PORT] [-d DATABASE]
    churz.py --help
    churz.py --version

Options:
    -p PORT      Port number [default: 9393].
    -d DATABASE  Database file [default: data.db].

"""
import os
import sys
import signal
import base64
import shelve
from bottle import get, post, run, redirect, request, abort, HTTPResponse
from docopt import docopt


@get('/')
@get('/<path:re:[a-zA-Z0-9_\-]+>')
def retrieve(path=None):
    """Redirect to real URL."""
    if path is None:
        return '<img src="http://i1.kym-cdn.com/photos/images/newsfeed/000/345/309/5eb.gif">'
    try:
        redirect(db[path], code=301)
    except KeyError as e:
        abort(404, 'URL %s not found.' % e)


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
    text = '{url}{rand}\n'.format(url=request.url, rand=rand_string)
    raise HTTPResponse(text, 201)


def sigint(signal, frame):
    """Handle SIGINT signal to properly close shelve."""
    global db
    db.close()
    sys.exit()
signal.signal(signal.SIGINT, sigint)


if __name__ == '__main__':
    args = docopt(__doc__, version='Churz v0.1')
    try:
        port = int(args['-p'])
    except ValueError:
        raise ValueError('Invalid port number: %s.' % args['-p'])
    global db
    db = shelve.open(str(args['-d']))
    run(host='localhost', port=port)
