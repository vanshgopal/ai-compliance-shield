import urllib.request
import json
import time

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# Step 1: Create a bash console
url = 'https://www.pythonanywhere.com/api/v0/user/{}/consoles/'.format(username)
data = json.dumps({'executable': '/bin/bash'}).encode('utf-8')
req = urllib.request.Request(url, data=data, method='POST')
req.add_header('Authorization', 'Token {}'.format(token))
req.add_header('Content-Type', 'application/json')

try:
    resp = urllib.request.urlopen(req)
    body = resp.read().decode()
    print('Console response: {}'.format(body))
    if body.strip():
        console_info = json.loads(body)
        console_id = console_info['id']
    else:
        print('Empty response, trying to list consoles...')
        req2 = urllib.request.Request(url)
        req2.add_header('Authorization', 'Token {}'.format(token))
        resp2 = urllib.request.urlopen(req2)
        consoles = json.loads(resp2.read().decode())
        print('Consoles: {}'.format(json.dumps(consoles, indent=2)))
        if consoles:
            console_id = consoles[0]['id']
        else:
            print('No consoles found')
            exit(1)
    print('Using console: {}'.format(console_id))
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print('Error: {} {}'.format(e.code, body))
    exit(1)

# Step 2: List files
time.sleep(2)
cmd_url = 'https://www.pythonanywhere.com/api/v0/user/{}/consoles/{}/send_command/'.format(username, console_id)
cmd = 'ls -la /home/vgsr/ai-compliance-shield/ && echo "---TEMPLATES---" && ls -la /home/vgsr/ai-compliance-shield/frontend/templates/ 2>/dev/null && echo "---STATIC---" && ls -la /home/vgsr/ai-compliance-shield/frontend/static/ 2>/dev/null && echo "---BACKEND---" && ls -la /home/vgsr/ai-compliance-shield/backend/ 2>/dev/null'
cmd_data = json.dumps({'command': cmd}).encode('utf-8')
req3 = urllib.request.Request(cmd_url, data=cmd_data, method='POST')
req3.add_header('Authorization', 'Token {}'.format(token))
req3.add_header('Content-Type', 'application/json')

try:
    resp3 = urllib.request.urlopen(req3)
    print('Command sent: {}'.format(resp3.read().decode()))
except urllib.error.HTTPError as e:
    print('Error sending: {} {}'.format(e.code, e.read().decode()))

# Step 3: Wait and get output
time.sleep(5)
output_url = 'https://www.pythonanywhere.com/api/v0/user/{}/consoles/{}/get_output/'.format(username, console_id)
req4 = urllib.request.Request(output_url)
req4.add_header('Authorization', 'Token {}'.format(token))

try:
    resp4 = urllib.request.urlopen(req4)
    output = resp4.read().decode()
    print('=== SERVER OUTPUT ===')
    print(output)
except urllib.error.HTTPError as e:
    print('Error getting output: {} {}'.format(e.code, e.read().decode()))
