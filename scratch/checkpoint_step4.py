import sys
sys.path.insert(0, '.')
import app

expected_endpoints = [
    # Auth
    'index', 'login', 'logout', 'profile',
    # Admin
    'manage_users', 'add_user', 'edit_user', 'delete_user',
    'manage_teams', 'edit_team', 'create_admin',
    # Issues
    'list_issues', 'view_issue', 'create_issue', 'edit_issue',
    'delete_issue', 'resolve_issue', 'update_issue',
    # Files
    'serve_file', 'serve_legacy_file',
    # History
    'my_history',
    # Dashboard
    'dashboard'
]

routes = {rule.endpoint: rule for rule in app.app.url_map.iter_rules()}

print(f"Checking Step 4 endpoints ({len(expected_endpoints)} endpoints)...")
for ep in expected_endpoints:
    assert ep in routes, f"MISSING ENDPOINT: {ep}"
    rule = routes[ep]
    print(f"  [PASS] {ep:<20} -> {rule.rule} {sorted(list(rule.methods))}")

all_rules = list(app.app.url_map.iter_rules())
print(f"\nTotal rules registered in url_map: {len(all_rules)}")
assert len(all_rules) == 152, f"Expected 152 total rules, got {len(all_rules)}"
print("ALL STEP 4 ENDPOINTS VERIFIED 100%!")
