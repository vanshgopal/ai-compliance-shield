import urllib.request
import json
import time

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'
headers = {'Authorization': 'Token {}'.format(token), 'Content-Type': 'application/json'}

def api_get(path):
    url = 'https://www.pythonanywhere.com/api/v0/user/{}{}'.format(username, path)
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Token {}'.format(token))
    return urllib.request.urlopen(req)

def api_post(path, data=None):
    url = 'https://www.pythonanywhere.com/api/v0/user/{}{}'.format(username, path)
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, method='POST')
    req.add_header('Authorization', 'Token {}'.format(token))
    req.add_header('Content-Type', 'application/json')
    return urllib.request.urlopen(req)

def api_delete(path):
    url = 'https://www.pythonanywhere.com/api/v0/user/{}{}'.format(username, path)
    req = urllib.request.Request(url, method='DELETE')
    req.add_header('Authorization', 'Token {}'.format(token))
    return urllib.request.urlopen(req)

# Step 1: Kill all existing consoles
print("=== Killing existing consoles ===")
try:
    resp = api_get('/consoles/')
    consoles = json.loads(resp.read().decode())
    print("Found {} consoles".format(len(consoles)))
    for c in consoles:
        cid = c['id']
        print("  Killing console {}...".format(cid))
        try:
            api_delete('/consoles/{}/'.format(cid))
            print("  Killed!")
        except Exception as e:
            print("  Error killing: {}".format(e))
except Exception as e:
    print("Error listing consoles: {}".format(e))

time.sleep(2)

# Step 2: Create new console
print("\n=== Creating new console ===")
try:
    resp = api_post('/consoles/', {'executable': '/bin/bash'})
    body = resp.read().decode()
    if body.strip():
        console_info = json.loads(body)
        console_id = console_info['id']
        print("Console created: {}".format(console_id))
    else:
        print("Empty response")
        exit(1)
except Exception as e:
    print("Error: {}".format(e))
    exit(1)

# Step 3: Run command
time.sleep(2)
print("\n=== Running directory check ===")
try:
    api_post('/consoles/{}/send_command/'.format(console_id), 
             {'command': 'echo "=== ROOT ===" && ls /home/vgsr/ai-compliance-shield/ && echo "=== TEMPLATES ===" && ls /home/vgsr/ai-compliance-shield/frontend/templates/ && echo "=== STATIC ===" && ls /home/vgsr/ai-compliance-shield/frontend/static/ && echo "=== BACKEND ===" && ls /home/vgsr/ai-compliance-shield/backend/'})
    print("Command sent")
except Exception as e:
    print("Error: {}".format(e))

# Step 4: Get output
time.sleep(5)
print("\n=== Output ===")
try:
    resp = api_get('/consoles/{}/get_output/'.format(console_id))
    print(resp.read().decode())
except Exception as e:
    print("Error: {}".format(e))
