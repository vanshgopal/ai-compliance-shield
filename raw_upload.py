import http.client
import ssl

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# Read a local file
local_path = r'C:\Users\pc\Desktop\ai-compliance-shield\frontend\static\robots.txt'
with open(local_path, 'rb') as f:
    content = f.read()

remote_path = '/api/v0/user/{}/files/home/vgsr/ai-compliance-shield/frontend/static/robots.txt'.format(username)

print('File size: {} bytes'.format(len(content)))
print('Uploading to: {}'.format(remote_path))

# Raw HTTP PUT
context = ssl.create_default_context()
conn = http.client.HTTPSConnection('www.pythonanywhere.com', context=context)

headers = {
    'Authorization': 'Token {}'.format(token),
    'Content-Type': 'application/octet-stream',
    'Content-Length': str(len(content)),
}

conn.request('PUT', remote_path, body=content, headers=headers)
response = conn.getresponse()

print('Status: {} {}'.format(response.status, response.reason))
body = response.read().decode('utf-8', errors='replace')
print('Response: {}'.format(body[:500]))

conn.close()
