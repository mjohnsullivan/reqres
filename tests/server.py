"""
Simple HTTP server for testing
"""

import sys, cgi, urlparse, logging
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process

class MyHandler(BaseHTTPRequestHandler):
    """
    Custom handler for HTTP GET/POST
    """

    def router(self, data=None):
        """
        Request routing
        """
        if self.path == '/test_get/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('TEST GET RESPONSE')
        elif self.path == '/test_post/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('TEST POST RESPONSE:' + str(data))
        else:
            raise IOError()

    def do_GET(self):
        """
        Handle GET requests
        """
        try:
            self.router()
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def _handle_urlencoded_post(self, data):
        """
        Parses out the data from an x-www-form-urlencoded POST
        """
        result = urlparse.parse_qs(data)
        if not result:
            result = data
        return result

    def _handle_multipart_post(self, fileObj, pdict):
        """
        Parses out the multipart sections from a multipart/form-data POST
        """
        return cgi.parse_multipart(fileObj, pdict)

    def do_POST(self):
        """
        Handle simple POST requests
        """
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'application/x-www-form-urlencoded':
            data = self._handle_urlencoded_post(self.rfile.read(int(self.headers['Content-Length'])))
        elif ctype == 'multipart/form-data':
            data = _handle_multipart_post(self.rfile, pdict)
        else:
            raise IOError('Unknown POST type')
        self.router(data)

class HTTPd(object):
    """
    httpd server
    """

    def __init__(self, host, port, nr_requests=0):
        """
        Creates a web server for the number of specified requests.
        If nr_requests is 0, it will server forever.
        """
        self._host = host
        self._port = port
        self._httpd_proc = Process(target=self._run_server, args=(nr_requests,))
        
    def start(self, blocking=False):
        """
        Starts the httpd server
        """
        self._httpd_proc.start()
        if blocking:
            self._httpd_proc.join()

    def stop(self):
        """
        Stops the httpd server
        """
        self._httpd_proc.terminate()
        self._httpd_proc.join()

    def _run_server(self, nr_requests=0):
        """
        Runs the web server for the number of specified requests.
        If nr_requests is 0, it will server forever.
        """
        try:
            httpd = HTTPServer((self._host, self._port), MyHandler)
            logging.info('HTTP server started')
            if not nr_requests:
                httpd.serve_forever()
            else:
                for i in xrange(nr_requests):
                    httpd.handle_request()
        except KeyboardInterrupt:
            logging.info('^C received, shutting down server')
            httpd.socket.close()
 
if __name__ == '__main__':
    if len(sys.argv) == 1:
        httpd = HTTPd('localhost', 8090)
        httpd.start(True)
    else:
        print 'python server.py'
