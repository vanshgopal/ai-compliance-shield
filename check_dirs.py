import os
import urllib.request

username = 'vgsr'
token = os.environ["PYTHONANYWHERE_API_TOKEN"]
# List root directory
for path in ['/home/vgsr/', '/home/vgsr/ai-compliance-shield/', '/home/vgsr/ai-compliance-shield/frontend/', '/home/vgsr/ai-compliance-shield/frontend/templates/', '/home/vgsr/ai-compliance-shield/backend/']:
    url = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}'.format(username, path)
    req = urllib.request.Request(url, headers={'Authorization': 'Token {}'.format(token)})
    try:
        resp = urllib.request.urlopen(req)
        print('=== {} ==='.format(path))
        print(resp.read().decode())
    except Exception as e:
        print('ERROR {}: {}'.format(path, e))
