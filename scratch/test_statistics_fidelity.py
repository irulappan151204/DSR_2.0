import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from extensions import db, cache
from models import User, Team

def run_tests():
    print("================================================================================")
    print("TESTING STATISTICS FIDELITY & ACCESS CONTROL")
    print("================================================================================")
    
    with app.app_context():
        # Find test users
        md_user = User.query.filter_by(role='MD').first()
        admin_user = User.query.filter_by(role='Admin').first()
        lead_t1 = User.query.filter_by(username='sujatha').first()
        lead_t2 = User.query.filter_by(username='sheebha').first()
        member_user = User.query.filter_by(username='anita').first()
        t3_user = User.query.filter_by(team_id=3).first()
        
        assert md_user, "MD user not found"
        assert lead_t1, "Team 1 Lead (sujatha) not found"
        assert lead_t2, "Team 2 Lead (sheebha) not found"
        assert member_user, "Team Member (anita) not found"

        md_id = str(md_user.user_id)
        admin_id = str(admin_user.user_id)
        lead_t1_id = str(lead_t1.user_id)
        lead_t2_id = str(lead_t2.user_id)
        member_id = str(member_user.user_id)
        t3_id = str(t3_user.user_id)

    with app.test_client() as client:
        # 1. Test unauthorized access (Team Member)
        print("\n--- 1. Access Control: Team Member (Forbidden) ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = member_id
            sess['_fresh'] = True
        resp = client.get('/statistics', follow_redirects=False)
        assert resp.status_code == 302, f"Expected 302 redirect for member, got {resp.status_code}"
        assert '/dashboard' in resp.headers.get('Location', '')
        print("  [PASS] Team Member correctly redirected to /dashboard.")

        # 2. Test MD access (Default yesterday)
        print("\n--- 2. MD Access: Default date ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = md_id
            sess['_fresh'] = True
        resp = client.get('/statistics')
        assert resp.status_code == 200, f"Expected 200 for MD, got {resp.status_code}"
        html = resp.data.decode('utf-8')
        assert 'Combined' in html
        assert 'Statistics Overview' in html or 'Academics Statistics' in html
        print(f"  [PASS] MD default GET: HTTP 200 ({len(resp.data)} bytes)")

        # 3. Test MD access (Specific date 2026-08-22)
        print("\n--- 3. MD Access: Historical date 2026-08-22 ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = md_id
            sess['_fresh'] = True
        resp = client.get('/statistics?date=2026-08-22&nature=all')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert '2026-08-22' in html
        print(f"  [PASS] MD historical date GET: HTTP 200 ({len(resp.data)} bytes)")

        # 4. Test MD access (Date Range)
        print("\n--- 4. MD Access: Date Range ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = md_id
            sess['_fresh'] = True
        resp = client.get('/statistics?start_date=2026-08-20&end_date=2026-08-23')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert '2026-08-20 to 2026-08-23' in html
        print(f"  [PASS] MD date range GET: HTTP 200 ({len(resp.data)} bytes)")

        # 5. Test MD access (Nature filter: Critical)
        print("\n--- 5. MD Access: Nature filter Critical ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = md_id
            sess['_fresh'] = True
        resp = client.get('/statistics?date=all&nature=critical')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'Critical' in html
        print(f"  [PASS] MD nature critical GET: HTTP 200 ({len(resp.data)} bytes)")

        # 6. Test Team 1 Lead access
        print("\n--- 6. Team 1 Lead Access ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = lead_t1_id
            sess['_fresh'] = True
        resp = client.get('/statistics?date=all')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'Academics Statistics' in html
        print(f"  [PASS] Team 1 Lead GET: HTTP 200 ({len(resp.data)} bytes)")

        # 7. Test Team 2 Lead access
        print("\n--- 7. Team 2 Lead Access ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = lead_t2_id
            sess['_fresh'] = True
        resp = client.get('/statistics?date=all')
        assert resp.status_code == 200
        html = resp.data.decode('utf-8')
        assert 'Admin Statistics' in html
        print(f"  [PASS] Team 2 Lead GET: HTTP 200 ({len(resp.data)} bytes)")

        # 8. Test Admin access
        print("\n--- 8. Admin Access ---")
        cache.clear()
        with client.session_transaction() as sess:
            sess['_user_id'] = admin_id
            sess['_fresh'] = True
        # Admin is not MD or Team Lead, should be denied
        resp = client.get('/statistics', follow_redirects=False)
        assert resp.status_code == 302
        assert '/dashboard' in resp.headers.get('Location', '')
        print("  [PASS] Admin without lead flag correctly redirected to /dashboard.")

    print("\n================================================================================")
    print("ALL STATISTICS FIDELITY TESTS PASSED (100%)!")
    print("================================================================================")

if __name__ == '__main__':
    run_tests()
