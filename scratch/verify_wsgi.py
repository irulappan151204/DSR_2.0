import sys
sys.path.insert(0, '.')

print("=" * 80)
print("WSGI PRODUCTION ENTRY POINT VERIFICATION")
print("=" * 80)

# 1. Verify file size and clean structure
import inspect
with open('wsgi.py', 'r') as f:
    wsgi_content = f.read()
print(f"wsgi.py line count: {len(wsgi_content.splitlines())}")
print(f"wsgi.py byte size:  {len(wsgi_content.encode('utf-8'))} bytes")
assert len(wsgi_content.splitlines()) <= 20, "wsgi.py should be a concise entry point!"

# 2. Import application
import wsgi
application = getattr(wsgi, 'application', None)
assert application is not None, "application not found in wsgi!"
print(f"  [PASS] Application imported successfully: {application}")

# 3. Verify Configuration
assert application.config.get('SECRET_KEY') is not None, "Missing SECRET_KEY!"
print(f"  [PASS] Configuration loaded: DB URI = {application.config.get('SQLALCHEMY_DATABASE_URI')}")

# 4. Verify Database Connection
with application.app_context():
    from extensions import db
    from sqlalchemy import text
    db_res = db.session.execute(text("SELECT 1")).scalar()
    assert db_res == 1, "Database connection failed via WSGI!"
    print(f"  [PASS] Database connection verified (SELECT 1 -> {db_res})")

# 5. Verify Registered Blueprints
expected_blueprints = {'md_dashboard', 'statistics', 'actions', 'critical', 'acknowledgements', 'report'}
registered_blueprints = set(application.blueprints.keys())
print(f"Registered Blueprints: {sorted(list(registered_blueprints))}")
for bp in expected_blueprints:
    assert bp in registered_blueprints, f"Missing blueprint: {bp}"
print("  [PASS] All core production blueprints registered.")

# 6. Verify Routes Available
routes = [rule.rule for rule in application.url_map.iter_rules()]
print(f"Total endpoints/routes available: {len(routes)}")
for r in ['/login', '/logout', '/dashboard', '/actions', '/critical', '/statistics', '/my_history']:
    assert r in routes, f"Missing route: {r}"
print("  [PASS] All critical application routes accessible.")

# 7. Test WSGI Client Request
with application.test_client() as client:
    resp = client.get('/login')
    assert resp.status_code == 200
    assert "login" in resp.data.decode('utf-8').lower()
    print("  [PASS] WSGI client request to /login returned HTTP 200.")

print("\n==========================================================")
print("ALL WSGI VERIFICATION TESTS PASSED (100%)!")
print("==========================================================")
