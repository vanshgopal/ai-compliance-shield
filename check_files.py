import urllib.request
import json

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'

# Try different possible paths
paths_to_check = [
    '/home/vgsr/ai-compliance-shield/frontend/static/robots.txt',
    '/home/vgsr/ai-compliance-shield/frontend/static/sitemap.xml',
    '/home/vgsr/ai-compliance-shield/backend/main.py',
    '/home/vgsr/ai-compliance-shield/run.py',
]

for path in paths_to_check:
    url = 'https://www.pythonanywhere.com/api/v0/user/{}/files{}'.format(username, path)
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Token {}'.format(token))
    try:
        resp = urllib.request.urlopen(req)
        content = resp.read().decode()
        # Check if it has GA4
        has_ga4 = 'G-QNZ5VNJ73M' in content
        has_old_ga4 = 'G-XXXXXXXXXX' in content
        has_old_date = '2026-08-30' in content
        print('OK: {} (GA4:{}, old_GA4:{}, old_date:{})'.format(path, has_ga4, has_old_ga4, has_old_date))
        # Print first 200 chars
        print('  Content preview: {}'.format(content[:200]))
    except urllib.error.HTTPError as e:
        print('ERROR {}: {}'.format(e.code, path))
    print()
