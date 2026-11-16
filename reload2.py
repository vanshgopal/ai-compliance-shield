import os
import urllib.request
import json

username = 'vgsr'
token = os.environ["PYTHONANYWHERE_API_TOKEN"]
# Reload the web app
url = f'https://www.pythonanywhere.com/api/v0/user/{username}/webapps/vgsr.pythonanywhere.com/reload/'
req = urllib.request.Request(url, method='POST')
req.add_header('Authorization', f'Token {token}')

try:
    response = urllib.request.urlopen(req)
    print('Reload:', response.read().decode())
except urllib.error.HTTPError as e:
    print(f'Error: {e.code}')
    print(f'Body: {e.read().decode()}')
