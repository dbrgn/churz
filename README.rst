########################################
Churz – Yet another simple URL shortener
########################################

*Churz* is yet another simple URL shortener in 33 SLOC.

It's written in Python using `Bottle`_ and `Shelve`_.

The name *Churz* is Swiss German for "short".

Run
===

::

    pip install -r requirements.txt
    python churz.py

Use
===

You can create new shortlinks by POSTing to ``/``. The URL to be shortened should
be provided in a ``url`` field in your POST data. The response will return the
short URL in the response body text.

License
=======

MIT License, see ``LICENSE`` file.


.. _Bottle: http://bottlepy.org/
.. _Shelve: http://docs.python.org/library/shelve.html
