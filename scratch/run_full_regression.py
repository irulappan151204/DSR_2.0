import sys
sys.path.insert(0, '.')
from app import app
from models import User, CapaFinding, CapaEvent
from extensions import db, cache
from datetime import date

print("=" * 80)
print("END-TO-END MASTER REGRESSION SUITE")
print("=" * 80)

with app.test_client() as client:
    # 1. LOGIN
    print("Step 1: Testing Login...")
    resp_login_get = client.get('/login')
    assert resp_login_get.status_code == 200
    
    with app.app_context():
        auditor = User.query.filter_by(username='auditteam').first()
        auditor_id = str(auditor.user_id)
        
    with client.session_transaction() as sess:
        sess['_user_id'] = auditor_id
        sess['_fresh'] = True
    print("  [PASS] Logged in successfully via session.")

    # 2. DASHBOARD
    print("Step 2: Testing Dashboard...")
    resp_dash = client.get('/md/dashboard?team=all')
    assert resp_dash.status_code == 200
    print(f"  [PASS] MD Dashboard HTTP 200 ({len(resp_dash.data)} bytes)")

    # 3. STATISTICS
    print("Step 3: Testing Statistics...")
    resp_stats = client.get('/statistics')
    assert resp_stats.status_code == 200
    print(f"  [PASS] Statistics HTTP 200 ({len(resp_stats.data)} bytes)")

    # 4. CRITICAL
    print("Step 4: Testing Critical List...")
    resp_crit = client.get('/critical')
    assert resp_crit.status_code == 200
    print(f"  [PASS] Critical Page HTTP 200 ({len(resp_crit.data)} bytes)")

    # 5. ACTIONS
    print("Step 5: Testing Actions...")
    resp_actions = client.get('/actions')
    assert resp_actions.status_code == 200
    print(f"  [PASS] Actions Page HTTP 200 ({len(resp_actions.data)} bytes)")

    # 6. HISTORY
    print("Step 6: Testing My History...")
    resp_hist = client.get('/my_history')
    assert resp_hist.status_code == 200
    print(f"  [PASS] History Page HTTP 200 ({len(resp_hist.data)} bytes)")

    # 7. CREATE FINDING
    print("Step 7: Creating Finding (Audit finding)...")
    with app.app_context():
        anita = User.query.filter_by(username='anita').first()
        anita_id = str(anita.user_id)
        
    create_payload = {
        'title': 'E2E Full Regression Audit Finding',
        'description': 'End-to-end regression validation issue',
        'nature_of_issue': 'All Well',
        'priority': 'Critical',
        'audit_date': date.today().isoformat(),
        'recipient_id': anita_id,
        'frequency': 'Monthly',
        'component': 'Academics',
        'audited_by': 'Audit Department',
        'staff_name': 'anita',
        'grade': 'Grade 10',
        'section': 'A',
        'specification': 'Final Exam Marksheets',
        'remark': 'All records must be verified by auditor'
    }
    resp_create = client.post('/critical/new', data=create_payload, follow_redirects=False)
    assert resp_create.status_code == 302
    finding_id = resp_create.headers['Location'].split('/')[-1]
    print(f"  [PASS] Finding created: ID {finding_id}")

    # 8. SWITCH USER -> ANITA RESPONDS WITH CAPA 1
    print("Step 8: Recipient submitting CAPA response...")
    with client.session_transaction() as sess:
        sess['_user_id'] = anita_id
        sess['_fresh'] = True
        
    resp_resp1 = client.post(f'/critical/{finding_id}/respond', data={
        'action_taken_report': 'All marksheets were compiled and verified.',
        'root_cause_analysis': 'Data entry delay during audit week.',
        'capa_1': 'Established automated daily marks sync procedure.'
    }, follow_redirects=False)
    assert resp_resp1.status_code == 302
    print("  [PASS] CAPA 1 response submitted.")

    # 9. SWITCH USER -> AUDITOR REVIEWS & REQUESTS REVISION
    print("Step 9: Auditor reviewing and requesting revision...")
    with app.app_context():
        auditor = User.query.filter_by(username='auditteam').first()
        auditor_id = str(auditor.user_id)
        
    with client.session_transaction() as sess:
        sess['_user_id'] = auditor_id
        sess['_fresh'] = True
        
    resp_rev1 = client.post(f'/critical/{finding_id}/review', data={
        'capa_2': 'Audit team notes on marksheet verification.',
        'audit_decision': 'NOT_ACCEPTED',
        'audit_justification': 'Please provide the sign-off record from the Academic Team Lead.'
    }, follow_redirects=False)
    assert resp_rev1.status_code == 302
    print("  [PASS] Revision requested with justification.")

    # 10. SWITCH USER -> ANITA RESUBMITS REVISED CAPA
    print("Step 10: Recipient resubmitting revised CAPA...")
    with client.session_transaction() as sess:
        sess['_user_id'] = anita_id
        sess['_fresh'] = True
        
    resp_resp2 = client.post(f'/critical/{finding_id}/respond', data={
        'action_taken_report': 'Marksheets verified and signed off by Academic Team Lead Sujatha.',
        'root_cause_analysis': 'Data entry delay during audit week addressed.',
        'capa_1': 'Implemented supervisor check on daily marksheet sign-off.'
    }, follow_redirects=False)
    assert resp_resp2.status_code == 302
    print("  [PASS] Revised CAPA resubmitted.")

    # 11. SWITCH USER -> AUDITOR ACCEPTS AND CLOSES
    print("Step 11: Auditor accepting revised CAPA and closing...")
    with client.session_transaction() as sess:
        sess['_user_id'] = auditor_id
        sess['_fresh'] = True
        
    resp_rev2 = client.post(f'/critical/{finding_id}/review', data={
        'capa_2': 'Verified Academic Lead sign-off. Corrective actions confirmed.',
        'audit_decision': 'ACCEPTED',
        'audit_justification': ''
    }, follow_redirects=False)
    assert resp_rev2.status_code == 302
    print("  [PASS] CAPA accepted and closed.")

    # 12. VERIFY FINAL DATABASE STATE
    print("Step 12: Verifying final finding status and event trail...")
    with app.app_context():
        finding = db.session.get(CapaFinding, int(finding_id))
        assert finding.status == 'CLOSED'
        assert finding.closed_at is not None
        assert finding.revision_count == 1
        
        events = CapaEvent.query.filter_by(finding_id=finding.form_id).order_by(CapaEvent.id).all()
        print(f"Total lifecycle events: {len(events)}")
        for e in events:
            print(f"  - {e.action} (User: {e.user.username if e.user else 'None'}): {e.comment}")
        assert len(events) == 5
        print("  [PASS] Final finding state: CLOSED with exact 5 lifecycle events.")

    # 13. LOGOUT
    print("Step 13: Testing Logout...")
    resp_logout = client.get('/logout', follow_redirects=False)
    assert resp_logout.status_code == 302
    print("  [PASS] Logged out successfully.")

print("\n" + "=" * 80)
print("ALL 13 MASTER REGRESSION WORKFLOW STEPS PASSED (100%)!")
print("=" * 80)
