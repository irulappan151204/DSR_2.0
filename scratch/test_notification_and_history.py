import sys
sys.path.insert(0, '.')
from app import app
from models import User, CapaFinding, CapaEvent
from critical import pending_critical_count
from extensions import db, cache
from datetime import date

with app.app_context():
    sujatha = User.query.filter_by(username='sujatha').first()   # Academic Lead (Team 1)
    anita = User.query.filter_by(username='anita').first()       # Academic Member (Team 1)
    sheebha = User.query.filter_by(username='sheebha').first()   # Admin Lead (Team 2)
    auditor = User.query.filter_by(username='auditteam').first() # Auditor

    initial_anita_cnt = pending_critical_count(anita)
    initial_sujatha_cnt = pending_critical_count(sujatha)
    initial_sheebha_cnt = pending_critical_count(sheebha)
    initial_auditor_cnt = pending_critical_count(auditor)

    print('Initial pending counts:')
    print(f'  Anita (Member T1):   {initial_anita_cnt}')
    print(f'  Sujatha (Lead T1):   {initial_sujatha_cnt}')
    print(f'  Sheebha (Lead T2):   {initial_sheebha_cnt}')
    print(f'  Auditor:             {initial_auditor_cnt}')

with app.test_client() as client:
    # 1. Auditor creates a finding assigned to anita
    with client.session_transaction() as sess:
        sess['_user_id'] = str(auditor.user_id)
        sess['_fresh'] = True

    post_data = {
        'title': 'Test Workflow Audit Finding',
        'description': 'Description of test issue',
        'nature_of_issue': 'All Well',
        'priority': 'High',
        'audit_date': date.today().isoformat(),
        'recipient_id': str(anita.user_id),
        'frequency': 'Monthly',
        'component': 'Academics',
        'audited_by': 'Internal Audit',
        'staff_name': anita.username,
        'grade': 'Grade 5',
        'section': 'A',
        'specification': 'Lesson Plan Verification',
        'remark': 'Requires immediate corrective action'
    }

    resp = client.post('/critical/new', data=post_data, follow_redirects=False)
    assert resp.status_code == 302
    created_id = resp.headers['Location'].split('/')[-1]
    print(f'\nCreated Finding Form ID: {created_id}')

    with app.app_context():
        finding = CapaFinding.query.get(int(created_id))
        assert finding is not None
        assert finding.status == 'PENDING_RECIPIENT_RESPONSE'

        events_on_create = CapaEvent.query.filter_by(finding_id=finding.form_id).all()
        print(f'Events on create: {len(events_on_create)}')
        for e in events_on_create:
            print(f'  - {e.action}: {e.comment}')
        assert len(events_on_create) == 1, f'Expected exactly 1 event on create, got {len(events_on_create)}'
        assert events_on_create[0].action == 'FINDING_CREATED'

        # Verify notification signal: Anita and Sujatha should have pending count incremented by 1, Sheebha should NOT
        print('\nPending counts after finding created:')
        anita_cnt = pending_critical_count(anita)
        sujatha_cnt = pending_critical_count(sujatha)
        sheebha_cnt = pending_critical_count(sheebha)
        print(f'  Anita (Member T1):   {anita_cnt}')
        print(f'  Sujatha (Lead T1):   {sujatha_cnt}')
        print(f'  Sheebha (Lead T2):   {sheebha_cnt}')
        assert anita_cnt == initial_anita_cnt + 1
        assert sujatha_cnt == initial_sujatha_cnt + 1
        assert sheebha_cnt == initial_sheebha_cnt, 'Sheebha (Admin Lead) count should not change!'

    # 2. Anita responds with CAPA 1
    with client.session_transaction() as sess:
        sess['_user_id'] = str(anita.user_id)
        sess['_fresh'] = True

    resp_data = {
        'action_taken_report': 'Corrective action taken immediately.',
        'root_cause_analysis': 'Lack of communication between staff.',
        'capa_1': 'Updated standard operating procedures.'
    }
    resp = client.post(f'/critical/{created_id}/respond', data=resp_data, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        finding = CapaFinding.query.get(int(created_id))
        assert finding.status == 'PENDING_AUDIT_REVIEW'

        events_after_resp = CapaEvent.query.filter_by(finding_id=finding.form_id).order_by(CapaEvent.id).all()
        print(f'\nEvents after response submitted: {len(events_after_resp)}')
        for e in events_after_resp:
            print(f'  - {e.action}: {e.comment}')
        assert len(events_after_resp) == 2, f'Expected exactly 2 events total, got {len(events_after_resp)}'
        assert events_after_resp[1].action == 'CAPA_RESPONSE_SUBMITTED'

        auditor_cnt = pending_critical_count(auditor)
        print(f'\nAuditor pending count after response: {auditor_cnt}')
        assert auditor_cnt >= 1

    # 3. Auditor accepts and closes finding
    with client.session_transaction() as sess:
        sess['_user_id'] = str(auditor.user_id)
        sess['_fresh'] = True

    review_data = {
        'capa_2': 'Verified SOP updates during re-audit.',
        'audit_decision': 'ACCEPTED',
        'audit_justification': ''
    }
    resp = client.post(f'/critical/{created_id}/review', data=review_data, follow_redirects=False)
    assert resp.status_code == 302

    with app.app_context():
        finding = CapaFinding.query.get(int(created_id))
        assert finding.status == 'CLOSED'

        events_final = CapaEvent.query.filter_by(finding_id=finding.form_id).order_by(CapaEvent.id).all()
        print(f'\nEvents after audit acceptance: {len(events_final)}')
        for e in events_final:
            print(f'  - {e.action}: {e.comment}')
        assert len(events_final) == 3, f'Expected exactly 3 clean milestones across full lifecycle, got {len(events_final)}'
        assert events_final[2].action == 'CAPA_ACCEPTED'

        print('\nALL NOTIFICATION & HISTORY WORKFLOW TESTS PASSED SUCCESSFULLY!')
