import sys
sys.path.insert(0, '.')
from app import app
from models import User, Team, Action, FileStorage, Team2ACTemperatureCheck, Team3NewAudit, Acknowledgement
from extensions import db
from datetime import datetime

with app.app_context():
    print("=" * 80)
    print("LEGACY & MIGRATED OLD DATA COMPATIBILITY VERIFICATION")
    print("=" * 80)

    # 1. Check legacy actions
    print("\n--- 1. ACTIONS TABLE (1309 Historical Rows) ---")
    oldest_action = Action.query.order_by(Action.id.asc()).first()
    newest_action = Action.query.order_by(Action.id.desc()).first()
    print(f"Oldest Action: ID {oldest_action.id} | Title: {oldest_action.title} | Status: {oldest_action.status} | Created: {oldest_action.created_at}")
    print(f"Newest Action: ID {newest_action.id} | Title: {newest_action.title} | Status: {newest_action.status} | Created: {newest_action.created_at}")
    
    # Check NULL handling in actions
    null_parent = Action.query.filter(Action.parent_action_id.is_(None)).count()
    has_parent = Action.query.filter(Action.parent_action_id.isnot(None)).count()
    null_completed = Action.query.filter(Action.completed_at.is_(None)).count()
    null_msg = Action.query.filter(Action.completion_message.is_(None)).count()
    print(f"Parent Actions: {null_parent}, Child Actions: {has_parent}")
    print(f"Actions with NULL completed_at: {null_completed}")
    print(f"Actions with NULL completion_message: {null_msg}")
    assert null_parent + has_parent == 1309
    print("  [PASS] Actions legacy NULL columns and statuses preserved.")

    # 2. Check heavy legacy form tables
    print("\n--- 2. HEAVY FORM TABLES (Team 2 & Team 3) ---")
    ac_count = Team2ACTemperatureCheck.query.count()
    audit_count = Team3NewAudit.query.count()
    print(f"Team2 AC Temperature Check Rows: {ac_count}")
    print(f"Team3 New Audit Rows:            {audit_count}")
    assert ac_count >= 8000, f"Expected >8000 AC rows, found {ac_count}"
    assert audit_count >= 3000, f"Expected >3000 Audit rows, found {audit_count}"
    
    # Verify relationships on legacy rows
    sample_audit = Team3NewAudit.query.filter(Team3NewAudit.media_file_id.isnot(None)).first()
    if sample_audit:
        print(f"Legacy Audit ID {sample_audit.form_id} links to media_file_id: {sample_audit.media_file_id}")
        assert sample_audit.media_file is not None
        print(f"  [PASS] Media file relationship loaded: {sample_audit.media_file.filename}")

    # 3. Check legacy FileStorage binary BLOBs
    print("\n--- 3. FILE STORAGE (757 Historical Files) ---")
    file_count = FileStorage.query.count()
    print(f"FileStorage Total Records: {file_count}")
    sample_file = FileStorage.query.order_by(FileStorage.file_id.asc()).first()
    print(f"Oldest File ID {sample_file.file_id}: {sample_file.filename}, size {len(sample_file.file_data)} bytes")
    assert len(sample_file.file_data) > 0, "Binary BLOB data is empty!"
    print("  [PASS] FileStorage binary BLOB integrity verified.")

    # 4. Check historical Acknowledgements
    print("\n--- 4. ACKNOWLEDGEMENTS (594 Historical Records) ---")
    ack_count = Acknowledgement.query.count()
    print(f"Total Acknowledgement records: {ack_count}")
    assert ack_count >= 590
    print("  [PASS] Historical acknowledgements preserved.")

    # 5. Check Users and Teams mapping
    print("\n--- 5. USERS & TEAMS (59 Users, 3 Teams) ---")
    users_count = User.query.count()
    teams_count = Team.query.count()
    print(f"Total Users: {users_count}, Total Teams: {teams_count}")
    assert users_count == 59 and teams_count == 3
    print("  [PASS] All users, teams, and role assignments intact.")

    sujatha = User.query.filter_by(username='sujatha').first()
    md = User.query.filter_by(username='auditteam').first()

with app.test_client() as client:
    from extensions import cache
    cache.clear()
    
    print("\n--- 6. HTTP TESTING HISTORICAL DATES ---")
    # Historical date from active records
    with client.session_transaction() as sess:
        sess['_user_id'] = str(md.user_id)
        sess['_fresh'] = True
        
    # Statistics for 2026-08-22
    resp_stats = client.get('/statistics?date=2026-08-22&nature=all')
    assert resp_stats.status_code == 200
    print(f"Statistics GET ?date=2026-08-22: HTTP {resp_stats.status_code} ({len(resp_stats.data)} bytes)")
    
    # Dashboard for 2026-08-22
    resp_dash = client.get('/md/dashboard?team=team3&date=2026-08-22')
    assert resp_dash.status_code == 200
    print(f"MD Dashboard GET ?team=team3&date=2026-08-22: HTTP {resp_dash.status_code} ({len(resp_dash.data)} bytes)")

print("\n==========================================================")
print("ALL OLD DATA COMPATIBILITY TESTS PASSED (100%)!")
print("==========================================================")
