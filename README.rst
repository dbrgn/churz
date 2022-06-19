Churz – Yet another simple URL shortener
========================================


*Churz* is yet another simple URL shortener in 40 SLOC.

It's written in Python 3 using `Bottle`_. Data is stored in a JSON file.

The name *Churz* is Swiss German for "short".


Install
-------

::

    $ pip install -r requirements.txt


Run
---

::

    Usage:
        churz.py [-p PORT] [-d DATABASE]
        churz.py --help
        churz.py --version

    Options:
        -p PORT      Port number [default: 9393].
        -d DATABASE  Database file [default: data.db].


Use
---

You can create new shortlinks by POSTing to ``/``. The URL to be shortened should
be provided in a ``url`` field in your POST data. The response will return the
short URL in the response body text. ::

    curl --data "url=http://www.youtube.com/watch?v=J---aiyznGQ" http://localhost:9393/


systemd
-------

There's a systemd unit file called ``churz.service`` that can be used to run and
monitor churz as a system service. You can use it as follows:

1. Adjust the path to the code and the virtualenv in the unit file
2. Copy the unit file to ``/etc/systemd/system/``
3. Run ``sudo systemctl start churz`` and ``sudo systemctl enable churz``

If you think a parametrizable unit file (think ``churz@-var-www-churz.service``)
would make sense, please open an issue on GitHub.


Dockerfile
----------

The provided Dockerfile starts the service on port ``9393``. The user's uid is
``14327`` and the data is on a volume mounted to ``/var/data``.


License
-------

MIT License, see ``LICENSE`` file.


.. _Bottle: http://bottlepy.org/
