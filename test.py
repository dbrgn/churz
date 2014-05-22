# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import unittest
import os
import subprocess
import signal
import time
import requests
import socket
import errno

URL = 'http://localhost:9393/'


def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port


class IntegrationTests(unittest.TestCase):

    def setUp(self):
        port = get_free_port()
        self.db = '%s.db' % time.time()
        print('Starting test server...')
        self.server = subprocess.Popen('python churz.py -p %s -d %s' % (port, self.db), shell=True)
        time.sleep(3)
        self.url = 'http://localhost:%u/' % port

    def tearDown(self):
        print('Stopping test server...')
        self.server.send_signal(signal.SIGINT)
        time.sleep(1)
        self.server.send_signal(signal.SIGKILL)
        self.server.wait()
        print('Removing test database')
        try:
            os.remove(os.path.abspath(self.db))
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


    def testHome(self):
        r = requests.get(self.url)
        self.assertTrue('<img' in r.content)

    def testStoreNew(self):
        data = {'url': 'http://github.com/'}
        r1 = requests.post(self.url, data)
        self.assertEqual(201, r1.status_code)
        url = r1.content
        r2 = requests.get(url)
        self.assertEqual(301, r2.history[0].status_code)
        self.assertEqual('https://github.com/', r2.url)

    def testNotFound(self):
        r = requests.get(self.url + 'foobar')
        self.assertEqual(404, r.status_code)


if __name__ == '__main__':
    unittest.main()
