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
    console_info = json.loads(resp.read().decode())
    console_id = console_info['id']
    print('Console created: {}'.format(console_id))
except urllib.error.HTTPError as e:
    print('Error creating console: {} {}'.format(e.code, e.read().decode()))
    exit(1)

# Step 2: Send a command - list the directory structure
cmd_url = 'https://www.pythonanywhere.com/api/v0/user/{}/consoles/{}/send_command/'.format(username, console_id)
cmd_data = json.dumps({'command': 'find /home/vgsr/ai-compliance-shield -type f -name "*.html" -o -name "*.xml" -o -name "*.py" -o -name "*.txt" | head -30'}).encode('utf-8')
req2 = urllib.request.Request(cmd_url, data=cmd_data, method='POST')
req2.add_header('Authorization', 'Token {}'.format(token))
req2.add_header('Content-Type', 'application/json')

try:
    resp2 = urllib.request.urlopen(req2)
    print('Command sent')
except urllib.error.HTTPError as e:
    print('Error sending command: {} {}'.format(e.code, e.read().decode()))

# Step 3: Wait and get output
time.sleep(3)
output_url = 'https://www.pythonanywhere.com/api/v0/user/{}/consoles/{}/get_output/'.format(username, console_id)
req3 = urllib.request.Request(output_url)
req3.add_header('Authorization', 'Token {}'.format(token))

try:
    resp3 = urllib.request.urlopen(req3)
    print('Output:')
    print(resp3.read().decode())
except urllib.error.HTTPError as e:
    print('Error getting output: {} {}'.format(e.code, e.read().decode()))
