import urllib.request
import os

username = 'vgsr'
token = 'c9cb9a6dea5fe56f86e5b317d44114fd591b28ce'
base_url = 'https://www.pythonanywhere.com/api/v0/user/{}/files'.format(username)

LOCAL = r'C:\Users\pc\Desktop\ai-compliance-shield'

files = [
    ('frontend/templates/index.html', '/home/vgsr/ai-compliance-shield/frontend/templates/index.html'),
    ('frontend/templates/pricing.html', '/home/vgsr/ai-compliance-shield/frontend/templates/pricing.html'),
    ('frontend/templates/features.html', '/home/vgsr/ai-compliance-shield/frontend/templates/features.html'),
    ('frontend/templates/how-it-works.html', '/home/vgsr/ai-compliance-shield/frontend/templates/how-it-works.html'),
    ('frontend/templates/about.html', '/home/vgsr/ai-compliance-shield/frontend/templates/about.html'),
    ('frontend/templates/contact.html', '/home/vgsr/ai-compliance-shield/frontend/templates/contact.html'),
    ('frontend/templates/resources.html', '/home/vgsr/ai-compliance-shield/frontend/templates/resources.html'),
    ('frontend/templates/privacy-policy.html', '/home/vgsr/ai-compliance-shield/frontend/templates/privacy-policy.html'),
    ('frontend/templates/terms.html', '/home/vgsr/ai-compliance-shield/frontend/templates/terms.html'),
    ('frontend/templates/refund-policy.html', '/home/vgsr/ai-compliance-shield/frontend/templates/refund-policy.html'),
    ('frontend/templates/blog/eu-ai-act-requirements-checklist-2026.html', '/home/vgsr/ai-compliance-shield/frontend/templates/blog/eu-ai-act-requirements-checklist-2026.html'),
    ('frontend/templates/blog/eu-ai-act-fines-2026.html', '/home/vgsr/ai-compliance-shield/frontend/templates/blog/eu-ai-act-fines-2026.html'),
    ('frontend/templates/blog/eu-ai-act-compliance-indian-saas-2026.html', '/home/vgsr/ai-compliance-shield/frontend/templates/blog/eu-ai-act-compliance-indian-saas-2026.html'),
    ('frontend/templates/blog/eu-ai-act-compliance-for-startups-2026.html', '/home/vgsr/ai-compliance-shield/frontend/templates/blog/eu-ai-act-compliance-for-startups-2026.html'),
    ('frontend/static/sitemap.xml', '/home/vgsr/ai-compliance-shield/frontend/static/sitemap.xml'),
    ('frontend/static/robots.txt', '/home/vgsr/ai-compliance-shield/frontend/static/robots.txt'),
    ('frontend/static/style.css', '/home/vgsr/ai-compliance-shield/frontend/static/style.css'),
    ('frontend/static/app.js', '/home/vgsr/ai-compliance-shield/frontend/static/app.js'),
    ('backend/main.py', '/home/vgsr/ai-compliance-shield/backend/main.py'),
    ('requirements.txt', '/home/vgsr/ai-compliance-shield/requirements.txt'),
    ('run.py', '/home/vgsr/ai-compliance-shield/run.py'),
]

for local_rel, remote_path in files:
    local_path = os.path.join(LOCAL, local_rel)
    if not os.path.exists(local_path):
        print('SKIP (not found): {}'.format(local_rel))
        continue

    with open(local_path, 'rb') as f:
        content = f.read()

    url = '{}{}'.format(base_url, remote_path)
    req = urllib.request.Request(url, data=content, method='PUT')
    req.add_header('Authorization', 'Token {}'.format(token))
    req.add_header('Content-Type', 'application/octet-stream')

    try:
        resp = urllib.request.urlopen(req)
        size = len(content)
        print('OK ({} bytes): {}'.format(size, remote_path))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print('ERROR {}: {} -> {}'.format(e.code, remote_path, body))

print('\nAll uploads complete!')
