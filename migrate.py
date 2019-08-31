"""
Migrate a Python2 shelve database to a JSON based database.

Usage:
    listdb.py <old.db> <new.json>
    listdb.py --help
    listdb.py --version

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import json
import sys
import signal
import shelve

from docopt import docopt


def sigint(signal, frame):
    """Handle SIGINT signal to properly close shelve."""
    global db_old
    db_old.close()
    sys.exit()
signal.signal(signal.SIGINT, sigint)


if __name__ == '__main__':
    args = docopt(__doc__, version='Churz v0.1')
    global db_old
    db_old = shelve.open(str(args['<old.db>']))
    data = {}
    for pair in db_old.items():
        print('%s -> %s' % pair)
        data[pair[0]] = pair[1]
    with open(str(args['<new.json>']), 'w') as db_new:
        db_new.write(json.dumps(data, indent=2))
    db_old.close()
