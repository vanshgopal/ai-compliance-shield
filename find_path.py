import os
import urllib.request
import json

username = 'vgsr'
token = os.environ["PYTHONANYWHERE_API_TOKEN"]
# Try listing home directory
paths_to_try = [
    '/home/vgsr/',
    '/home/vgsr/ai-compliance-shield/',
    '/home/vgsr/ai_compliance_shield/',
]

for path in paths_to_try:
    url = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}'.format(username, path)
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Token {}'.format(token))
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        print('=== {} ==='.format(path))
        print(content[:500])
    except urllib.error.HTTPError as e:
        print('ERROR {}: {}'.format(e.code, path))
    print()
