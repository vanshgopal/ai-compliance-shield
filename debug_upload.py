import urllib.request
import json

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# First, try to create directories by uploading to them
# The PUT API creates parent directories automatically
# But we need to check if the source_directory is correct

# Read the webapp info
url = 'https://www.pythonanywhere.com/api/v0/user/{}/webapps/vgsr.pythonanywhere.com/'.format(username)
req = urllib.request.Request(url)
req.add_header('Authorization', 'Token {}'.format(token))
try:
    resp = urllib.request.urlopen(req)
    info = json.loads(resp.read().decode())
    print('Source directory: {}'.format(info.get('source_directory', 'N/A')))
    print('Working directory: {}'.format(info.get('working_directory', 'N/A')))
    print('Python version: {}'.format(info.get('python_version', 'N/A')))
except urllib.error.HTTPError as e:
    print('Error: {} {}'.format(e.code, e.read().decode()[:200]))

# Now try writing a test file to source_directory path
print('\n--- Testing upload to source directory ---')
test_path = '{}/test_seo.txt'.format(info.get('source_directory', '/home/vgsr'))
url2 = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}'.format(username, test_path)
data = b'test content'
req2 = urllib.request.Request(url2, data=data, method='PUT')
req2.add_header('Authorization', 'Token {}'.format(token))
req2.add_header('Content-Type', 'application/octet-stream')
try:
    resp2 = urllib.request.urlopen(req2)
    print('Write OK: {}'.format(resp2.read().decode()))
except urllib.error.HTTPError as e:
    body = e.read().decode()[:200]
    print('Write error {}: {}'.format(e.code, body))

# Read it back
req3 = urllib.request.Request(url2)
req3.add_header('Authorization', 'Token {}'.format(token))
try:
    resp3 = urllib.request.urlopen(req3)
    print('Read OK: {}'.format(resp3.read().decode()))
except urllib.error.HTTPError as e:
    print('Read error {}: {}'.format(e.code, e.read().decode()[:200]))

# Also try listing files in the source directory
print('\n--- Listing source directory ---')
url4 = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}/'.format(username, info.get('source_directory', '/home/vgsr'))
req4 = urllib.request.Request(url4)
req4.add_header('Authorization', 'Token {}'.format(token))
try:
    resp4 = urllib.request.urlopen(req4)
    print('Files: {}'.format(resp4.read().decode()[:500]))
except urllib.error.HTTPError as e:
    print('List error {}: {}'.format(e.code, e.read().decode()[:200]))
