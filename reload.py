import os
import urllib.request
import json

username = 'vgsr'
token = os.environ["PYTHONANYWHERE_API_TOKEN"]
# Step 1: List webapps
url = f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/'
req = urllib.request.Request(url, method='GET')
req.add_header('Authorization', f'Token {token}')

try:
    response = urllib.request.urlopen(req)
    print('Webapps:', response.read().decode())
except urllib.error.HTTPError as e:
    print(f'Error: {e.code}')
    print(f'Body: {e.read().decode()}')
