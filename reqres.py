"""
Implments a GET/POST wrapper for simple HTTP/HTTPS requests.

Includes multipart/form-data POST which is adapted from:
http://code.activestate.com/recipes/146306-http-client-to-post-using-multipartform-data/

Copyright 2012 Matt Sullivan

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import urllib2
import mimetypes
import base64

def get(url, data=None, credentials=None):
    """
    Open a url with optional basic auth credentials
    Credentials are of the form (username, password,)
    """
    req = urllib2.Request(url, data)
    _add_auth_header(req, credentials) 
    return urllib2.urlopen(req, timeout=5)

def post(url, data, credentials=None):
    """
    Open a URL and POST data
    """
    return get(url, data, credentials)  

def post_multipart(url, fields = [], files = [], credentials=None):
    """
    urllib2 implementation
    """
    content_type, body = _encode_multipart_formdata(fields, files)
    req = urllib2.Request(url, body)
    req.add_header('Content-type', content_type)
    _add_auth_header(req, credentials)
    return urllib2.urlopen(req, timeout=5)

def _add_auth_header(req, credentials):
    """
    Adds an Authentication header to a request
    
    The reason I'm not using the standard password manager stuff in
    urllib2 is because of the following:
     
    The Python libraries, per HTTP-Standard, first send an unauthenticated request,
    and then only if it's answered with a 401 retry, are the correct credentials sent.
    If the server doesn't do 'standard authentication' then the libraries won't work.
    """
    if credentials:
        base64str = base64.encodestring('%s:%s' % (credentials[0], credentials[1])).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64str)

def _encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for use in urllib2 requests
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % _get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def _get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
