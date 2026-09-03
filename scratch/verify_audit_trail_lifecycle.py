import sys
sys.path.insert(0, '.')
from app import app
from models import User, CapaFinding, CapaEvent
from extensions import db, cache
from datetime import date

with app.app_context():
    auditor = User.query.filter_by(username='auditteam').first()
    anita = User.query.filter_by(username='anita').first()
    
    print("--- 1. VERIFYING EXISTING HISTORICAL CAPA EVENTS ARE READABLE ---")
    all_events = CapaEvent.query.order_by(CapaEvent.id).all()
    print(f"Total existing CapaEvent records in DB: {len(all_events)}")
    assert len(all_events) > 0, "No historical events in DB!"
    for ev in all_events[:5]:
        print(f"  Event ID {ev.id}: Finding {ev.finding_id} | Action: {ev.action} | User: {ev.user.username if ev.user else 'None'} | Status: {ev.old_status} -> {ev.new_status}")
    print("  [PASS] Existing historical event records are intact and readable.")

with app.test_client() as client:
    print("\n--- 2. TESTING REVISION WORKFLOW (BRANCH B) ---")
    # Step 2A: Auditor creates finding
    with client.session_transaction() as sess:
        sess['_user_id'] = str(auditor.user_id)
        sess['_fresh'] = True
    
    post_data = {
        'title': 'Audit Finding Lifecycle Branch B Test',
        'description': 'Testing revision requested lifecycle',
        'nature_of_issue': 'All Well',
        'priority': 'Medium',
        'audit_date': date.today().isoformat(),
        'recipient_id': str(anita.user_id),
        'frequency': 'Quarterly',
        'component': 'Academics',
        'audited_by': 'Internal Audit',
        'staff_name': anita.username,
        'grade': 'Grade 6',
        'section': 'B',
        'specification': 'Attendance Records',
        'remark': 'Test remark'
    }
    resp = client.post('/critical/new', data=post_data, follow_redirects=False)
    assert resp.status_code == 302
    fid = resp.headers['Location'].split('/')[-1]
    
    with app.app_context():
        evs_1 = CapaEvent.query.filter_by(finding_id=int(fid)).all()
        print(f"Step 2A (Create): Events = {len(evs_1)}")
        assert len(evs_1) == 1, f"Expected 1 event, got {len(evs_1)}"
        assert evs_1[0].action == 'FINDING_CREATED'
        print(f"  [PASS] Exactly 1 event logged: {evs_1[0].action}")

    # Step 2B: Anita responds with CAPA 1
    with client.session_transaction() as sess:
        sess['_user_id'] = str(anita.user_id)
        sess['_fresh'] = True
    resp = client.post(f'/critical/{fid}/respond', data={
        'action_taken_report': 'First action taken report',
        'root_cause_analysis': 'First root cause analysis',
        'capa_1': 'First CAPA submission'
    }, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        evs_2 = CapaEvent.query.filter_by(finding_id=int(fid)).order_by(CapaEvent.id).all()
        print(f"Step 2B (Respond): Total Events = {len(evs_2)}")
        assert len(evs_2) == 2, f"Expected 2 events, got {len(evs_2)}"
        assert evs_2[1].action == 'CAPA_RESPONSE_SUBMITTED'
        print(f"  [PASS] Exactly 1 new event logged: {evs_2[1].action}")

    # Step 2C: Auditor requests REVISION
    with client.session_transaction() as sess:
        sess['_user_id'] = str(auditor.user_id)
        sess['_fresh'] = True
    resp = client.post(f'/critical/{fid}/review', data={
        'capa_2': 'Audit initial review notes requiring deeper root cause analysis.',
        'audit_decision': 'NOT_ACCEPTED',
        'audit_justification': 'Need more detail on root cause analysis'
    }, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        evs_3 = CapaEvent.query.filter_by(finding_id=int(fid)).order_by(CapaEvent.id).all()
        print(f"Step 2C (Revision Requested): Total Events = {len(evs_3)}")
        assert len(evs_3) == 3, f"Expected 3 events, got {len(evs_3)}"
        assert evs_3[2].action == 'CAPA_REVISION_REQUESTED'
        assert 'Need more detail' in evs_3[2].comment
        print(f"  [PASS] Exactly 1 new event logged: {evs_3[2].action} with justification.")

    # Step 2D: Anita resubmits revision
    with client.session_transaction() as sess:
        sess['_user_id'] = str(anita.user_id)
        sess['_fresh'] = True
    resp = client.post(f'/critical/{fid}/respond', data={
        'action_taken_report': 'Revised action taken report with detail',
        'root_cause_analysis': 'Deep root cause analysis provided',
        'capa_1': 'Revised preventive measure implemented'
    }, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        evs_4 = CapaEvent.query.filter_by(finding_id=int(fid)).order_by(CapaEvent.id).all()
        print(f"Step 2D (Resubmit Revision): Total Events = {len(evs_4)}")
        assert len(evs_4) == 4, f"Expected 4 events, got {len(evs_4)}"
        assert evs_4[3].action == 'CAPA_RESUBMITTED'
        print(f"  [PASS] Exactly 1 new event logged: {evs_4[3].action}")

    # Step 2E: Auditor accepts revised CAPA
    with client.session_transaction() as sess:
        sess['_user_id'] = str(auditor.user_id)
        sess['_fresh'] = True
    resp = client.post(f'/critical/{fid}/review', data={
        'capa_2': 'Verified comprehensive root cause and implementation.',
        'audit_decision': 'ACCEPTED',
        'audit_justification': ''
    }, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        evs_5 = CapaEvent.query.filter_by(finding_id=int(fid)).order_by(CapaEvent.id).all()
        print(f"Step 2E (Acceptance): Total Events = {len(evs_5)}")
        assert len(evs_5) == 5, f"Expected 5 events, got {len(evs_5)}"
        assert evs_5[4].action == 'CAPA_ACCEPTED'
        print(f"  [PASS] Exactly 1 new event logged: {evs_5[4].action}")

print("\n==========================================================")
print("ALL CAPA AUDIT TRAIL LIFECYCLE TESTS PASSED (100%)!")
print("==========================================================")
