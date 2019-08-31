"""Churz. Yet another simple URL shortener.

Warning: Probably not thread safe, so multiple stores at the same time might
get lost.

Usage:
    churz.py [-p PORT] [-d DATABASE]
    churz.py --help
    churz.py --version

Options:
    -p PORT      Port number [default: 9393].
    -d DATABASE  Database file, will be created if missing [default: data.db].

"""
import base64
from bottle import get, post, run, redirect, request, abort, HTTPResponse
from docopt import docopt
import json
import os


@get('/')
@get('/<path:re:[a-zA-Z0-9_\\-]+>')
def retrieve(path=None):
    """Redirect to real URL."""
    global db
    if path is None:
        return '<img src="http://i1.kym-cdn.com/photos/images/newsfeed/000/345/309/5eb.gif">'
    try:
        redirect(db[path], code=301)
    except KeyError as e:
        abort(404, 'URL %s not found.' % e)


@post('/')
def store():
    """Shorten new URL."""
    global db
    url = request.POST.get('url')
    while 1:
        rand_bytes = os.urandom(3)
        rand_string = base64.urlsafe_b64encode(rand_bytes).decode('ascii')
        if rand_string not in db:
            db[rand_string] = url
            with open(db_filename, 'w') as f:
                f.write(json.dumps(db, indent=2))
            break
    text = '{url}{rand}\n'.format(url=request.url, rand=rand_string)
    raise HTTPResponse(text, 201)


if __name__ == '__main__':
    args = docopt(__doc__, version='Churz v0.1')
    try:
        port = int(args['-p'])
    except ValueError:
        raise ValueError('Invalid port number: %s.' % args['-p'])
    global db, db_filename
    db_filename = args['-d']
    try:
        with open(db_filename, 'r') as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {}
    run(host='localhost', port=port)
