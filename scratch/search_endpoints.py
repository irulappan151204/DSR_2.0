import glob
import re

html_files = glob.glob('templates/**/*.html', recursive=True)
endpoints = [
    'login', 'logout', 'profile', 'dashboard', 'my_history',
    'manage_users', 'add_user', 'edit_user', 'delete_user',
    'manage_teams', 'edit_team', 'create_admin', 'list_issues',
    'view_issue', 'create_issue', 'edit_issue', 'delete_issue',
    'resolve_issue', 'update_issue', 'serve_file', 'serve_legacy_file'
]
usages = {}
for hf in html_files:
    with open(hf, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    for ep in endpoints:
        pattern = r"url_for\(['\"]" + ep + r"['\"]"
        if re.search(pattern, c):
            usages.setdefault(ep, []).append(hf)

print("Endpoint usages in templates:")
for ep in endpoints:
    files = usages.get(ep, [])
    print(f"  {ep:<20}: {len(files)} template files")
