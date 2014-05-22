"""
List all URLs in the shelve database.

Usage:
    listdb.py <database>
    listdb.py --help
    listdb.py --version

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import signal
import shelve

from docopt import docopt


def sigint(signal, frame):
    """Handle SIGINT signal to properly close shelve."""
    global db
    db.close()
    sys.exit()
signal.signal(signal.SIGINT, sigint)


if __name__ == '__main__':
    args = docopt(__doc__, version='Churz v0.1')
    global db
    db = shelve.open(str(args['<database>']))
    for pair in db.iteritems():
        print('%s -> %s' % pair)
    db.close()
