"""
Tests basic request/response
"""

import unittest, time
from urllib2 import HTTPError

import reqres as http

from tests.server import HTTPd

HOST = 'localhost'
PORT = 8090
BASE_URL = 'http://%s:%d' % (HOST, PORT)

class TestRequest(unittest.TestCase):
    """
    Basic HTTP request and response tests
    """

    def setUp(self):
        """
        Set up and start the httpd server
        """
        print 'Setting up HTTP server'
        self._httpd = HTTPd(HOST, PORT)
        self._httpd.start()
        time.sleep(0.5)

    def tearDown(self):
        """
        Shut down the httpd server
        """
        self._httpd.stop()

    def test_get_request(self):
        """
        Tests a simple GET request
        """
        resp = http.get(BASE_URL + '/test_get/')
        self.assertEqual(resp.read(), 'TEST GET RESPONSE')

    def test_post_request_urlencoded(self):
        """
        Tests a urlencoded POST
        """
        post_data = 'This is some test data'
        resp = http.post(BASE_URL + '/test_post/', post_data)
        self.assertEqual(resp.read(), 'TEST POST RESPONSE:' + post_data)

    def test_404(self):
        """
        Tests getting a 404 error in the response
        """
        self.assertRaises(HTTPError, http.get, BASE_URL + '/invalid_url')
