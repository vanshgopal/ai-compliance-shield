import urllib.request

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# The webapp source is /home/vgsr/ai-compliance-shield
# Try to read main.py from there
url = 'https://www.pythonanywhere.com/api/v0/user/{}/files/home/vgsr/ai-compliance-shield/backend/main.py'.format(username)
req = urllib.request.Request(url)
req.add_header('Authorization', 'Token {}'.format(token))

try:
    resp = urllib.request.urlopen(req)
    content = resp.read().decode()
    # Check if it has the new routes
    has_get_started = '/get-started' in content
    has_resources = '/resources' in content
    has_blog_route = '/blog/{slug}' in content
    print('main.py found!')
    print('Has /get-started route: {}'.format(has_get_started))
    print('Has /resources route: {}'.format(has_resources))
    print('Has /blog/{{slug}} route: {}'.format(has_blog_route))
    print()
    # Print lines with route definitions
    for line in content.split('\n'):
        if '@app.get' in line or '@app.post' in line:
            print(line.strip())
except urllib.error.HTTPError as e:
    print('ERROR {}: main.py not found'.format(e.code))

# Also try reading the old path
print()
url2 = 'https://www.pythonanywhere.com/api/v0/user/{}/files/home/vgsr/ai-compliance-shield/main.py'.format(username)
req2 = urllib.request.Request(url2)
req2.add_header('Authorization', 'Token {}'.format(token))
try:
    resp2 = urllib.request.urlopen(req2)
    content2 = resp2.read().decode()
    print('main.py at root found! (old structure)')
    print('First 300 chars: {}'.format(content2[:300]))
except urllib.error.HTTPError as e:
    print('ERROR {}: no main.py at root'.format(e.code))
