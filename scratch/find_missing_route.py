import sys
sys.path.insert(0, '.')
import subprocess
import re
import app

old_app = subprocess.check_output(['git', 'show', '0d72caf:app.py'], text=True, encoding='utf-8')

old_routes = set(re.findall(r"@app\.route\(['\"]([^'\"]+)['\"]", old_app))
current_routes = set([r.rule for r in app.app.url_map.iter_rules()])

missing = old_routes - current_routes
print(f"Routes in baseline missing from current: {missing}")

# Check endpoint counts
all_current_endpoints = {r.endpoint: r.rule for r in app.app.url_map.iter_rules()}
print(f"Total rules in url_map: {len(all_current_endpoints)}")
