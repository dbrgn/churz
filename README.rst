########################################
Churz – Yet another simple URL shortener
########################################

*Churz* is yet another simple URL shortener in 42 SLOC.

It's written in Python using `Bottle`_ and `Shelve`_.

The name *Churz* is Swiss German for "short".

Install
=======

::

    $ pip install -r requirements.txt

Run
===

::

    Usage:
        churz.py [-p PORT] [-d DATABASE]
        churz.py --help
        churz.py --version

    Options:
        -p PORT      Port number [default: 9393].
        -d DATABASE  Database file [default: data.db].

Use
===

You can create new shortlinks by POSTing to ``/``. The URL to be shortened should
be provided in a ``url`` field in your POST data. The response will return the
short URL in the response body text. ::

    curl --data "url=http://www.youtube.com/watch?v=J---aiyznGQ" http://localhost:9393/

License
=======

MIT License, see ``LICENSE`` file.


.. _Bottle: http://bottlepy.org/
.. _Shelve: http://docs.python.org/library/shelve.html
