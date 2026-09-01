import urllib.request
import json
import time

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'
console_id = 48016756

def api_call(method, path, data=None):
    url = 'https://www.pythonanywhere.com/api/v0/user/{}{}'.format(username, path)
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header('Authorization', 'Token {}'.format(token))
    req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req)
        return resp.read().decode()
    except urllib.error.HTTPError as e:
        return 'ERROR {}: {}'.format(e.code, e.read().decode()[:200])

# Send commands to check the directory structure
cmds = [
    'ls /home/vgsr/ai-compliance-shield/',
    'ls /home/vgsr/ai-compliance-shield/frontend/',
    'ls /home/vgsr/ai-compliance-shield/frontend/templates/',
    'ls /home/vgsr/ai-compliance-shield/frontend/templates/blog/',
    'ls /home/vgsr/ai-compliance-shield/frontend/static/',
]

for cmd in cmds:
    result = api_call('POST', '/consoles/{}/send_command/'.format(console_id), {'command': cmd})
    print('> {}'.format(cmd))
    print('  {}'.format(result))

time.sleep(3)

# Get output
result = api_call('GET', '/consoles/{}/get_output/'.format(console_id))
print('\n=== OUTPUT ===')
print(result)
