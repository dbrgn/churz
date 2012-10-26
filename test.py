import unittest
import os
import subprocess
import signal
import time
import requests

URL = 'http://localhost:9393/'

def server():
    """Server function that runs in background."""

class IntegrationTests(unittest.TestCase):

    def setUp(self):
        port = 39393
        self.db = '%s.db' % time.time()
        print 'Starting test server...'
        self.server = subprocess.Popen('python churz.py -p %s -d %s' % (port, self.db), shell=True)
        time.sleep(2)
        #self.url = 'http://localhost:%u/' % port
        self.url = 'http://localhost:9393/'

    def tearDown(self):
        print 'Stopping test server...'
        self.server.send_signal(signal.SIGINT)
        self.server.wait()
        print 'Removing test database'
        os.remove(os.path.abspath(self.db))

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
