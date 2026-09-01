import urllib.request
import json

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# Try to write a small test file and read it back
test_content = 'SEO_TEST_FILE'
test_path = '/home/vgsr/seo_test.txt'

# Write test file
url = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}'.format(username, test_path)
data = test_content.encode('utf-8')
req = urllib.request.Request(url, data=data, method='PUT')
req.add_header('Authorization', 'Token {}'.format(token))
req.add_header('Content-Type', 'application/octet-stream')

try:
    resp = urllib.request.urlopen(req)
    print('Write result: {} {}'.format(resp.status, resp.read().decode()))
except urllib.error.HTTPError as e:
    print('Write error: {} {}'.format(e.code, e.read().decode()))

# Read it back
req2 = urllib.request.Request(url)
req2.add_header('Authorization', 'Token {}'.format(token))
try:
    resp2 = urllib.request.urlopen(req2)
    print('Read back: {}'.format(resp2.read().decode()))
except urllib.error.HTTPError as e:
    print('Read error: {} {}'.format(e.code, e.read().decode()))
