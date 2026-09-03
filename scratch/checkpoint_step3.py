import sys
sys.path.insert(0, '.')

import app

routes = []
for rule in app.app.url_map.iter_rules():
    routes.append((rule.rule, rule.endpoint, sorted(list(rule.methods))))

print(f"Total routes registered: {len(routes)}")
assert len(routes) == 152, f"Expected 152 routes, got {len(routes)}"

# Check that submit routes exist and have exact same endpoints
submit_routes = [r for r in routes if 'submit' in r[0]]
print(f"Total submit routes: {len(submit_routes)}")
assert len(submit_routes) == 108, f"Expected 108 submit routes, got {len(submit_routes)}"

# Check key endpoints
endpoints = [r[1] for r in routes]
for key_endpoint in [
    'submit_team1_calendar', 'submit_team1_asa', 'submit_student_attendance',
    'submit_hr_attendance', 'submit_materials_inward', 'submit_camera_footage',
    'submit_team3_audit', 'submit_new_audit'
]:
    assert key_endpoint in endpoints, f"Missing endpoint: {key_endpoint}"
    print(f"  [PASS] Endpoint '{key_endpoint}' is registered.")

print("\nStep 3 Route Parity Check Passed 100%!")
