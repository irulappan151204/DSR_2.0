import sys
sys.path.insert(0, '.')
from app import app
from models import User, CapaFinding
from critical import visible_findings_query
from extensions import db, cache

with app.app_context():
    sujatha = User.query.filter_by(username='sujatha').first()   # Academic Lead (Team 1)
    anita = User.query.filter_by(username='anita').first()       # Academic Member (Team 1)
    sheebha = User.query.filter_by(username='sheebha').first()   # Admin Lead (Team 2)
    sathish = User.query.filter_by(username='sathish').first()   # Admin Member (Team 2)
    md = User.query.filter_by(username='auditteam').first()      # MD (Executive)
    admin = User.query.filter_by(username='admin').first()       # System Admin

    print("=" * 80)
    print("BACKEND QUERY-LEVEL CRITICAL / CAPA VISIBILITY VERIFICATION")
    print("=" * 80)
    
    # 1. Total findings in database
    all_findings = CapaFinding.query.all()
    print(f"Total Findings in DB: {len(all_findings)}")
    for f in all_findings:
        print(f"  Finding ID {f.form_id} ({f.audit_reference}) | Recipient: {f.recipient.username} (Team {f.recipient.team_id}) | Staff: {f.staff_name}")
        
    print("\n--- 1. TEAM MEMBER (Anita - Team 1) ---")
    anita_findings = visible_findings_query(anita).all()
    print(f"Anita visible findings count: {len(anita_findings)}")
    for f in anita_findings:
        assert f.recipient_id == anita.user_id or f.staff_name == anita.username, f"Unauthorized finding {f.audit_reference} visible to Anita!"
        print(f"  [PASS] Visible: {f.audit_reference} (assigned to {f.recipient.username})")
    print("  [VERIFIED] Anita sees ONLY her own authorized findings.")

    print("\n--- 2. TEAM LEAD (Sujatha - Academics / Team 1) ---")
    sujatha_findings = visible_findings_query(sujatha).all()
    print(f"Sujatha visible findings count: {len(sujatha_findings)}")
    sujatha_visible_refs = [f.audit_reference for f in sujatha_findings]
    for f in sujatha_findings:
        is_t1_recipient = (f.recipient and f.recipient.team_id == 1)
        is_t1_staff = f.staff_name in [u.username for u in User.query.filter_by(team_id=1).all()]
        is_sujatha_direct = (f.recipient_id == sujatha.user_id or f.submitted_by == sujatha.user_id)
        assert is_t1_recipient or is_t1_staff or is_sujatha_direct, f"Unauthorized non-team1 finding {f.audit_reference} visible to Sujatha!"
        print(f"  [PASS] Visible: {f.audit_reference} (Recipient: {f.recipient.username}, Team: {f.recipient.team_id}, Staff: {f.staff_name})")
    
    # Verify non-team1 findings are NOT in Sujatha's query
    admin_team_findings = CapaFinding.query.filter(CapaFinding.recipient_id == sathish.user_id).all()
    for atf in admin_team_findings:
        assert atf.audit_reference not in sujatha_visible_refs, f"SECURITY LEAK: Admin team finding {atf.audit_reference} was visible to Academic Lead!"
        print(f"  [SECURITY VERIFIED] Admin member finding {atf.audit_reference} is EXCLUDED from Academic Lead query.")

    print("\n--- 3. TEAM LEAD (Sheebha - Admin / Team 2) ---")
    sheebha_findings = visible_findings_query(sheebha).all()
    sheebha_visible_refs = [f.audit_reference for f in sheebha_findings]
    print(f"Sheebha visible findings count: {len(sheebha_findings)}")
    for f in sheebha_findings:
        is_t2_recipient = (f.recipient and f.recipient.team_id == 2)
        is_t2_staff = f.staff_name in [u.username for u in User.query.filter_by(team_id=2).all()]
        is_sheebha_direct = (f.recipient_id == sheebha.user_id or f.submitted_by == sheebha.user_id)
        assert is_t2_recipient or is_t2_staff or is_sheebha_direct, f"Unauthorized non-team2 finding {f.audit_reference} visible to Sheebha!"
        print(f"  [PASS] Visible: {f.audit_reference} (Recipient: {f.recipient.username}, Team: {f.recipient.team_id}, Staff: {f.staff_name})")
        
    for f1 in anita_findings:
        assert f1.audit_reference not in sheebha_visible_refs, f"SECURITY LEAK: Academic finding {f1.audit_reference} was visible to Admin Lead!"
    print("  [SECURITY VERIFIED] Academic member findings are EXCLUDED from Admin Lead query.")

    print("\n--- 4. MD & ADMIN (Auditteam & Admin) ---")
    md_findings = visible_findings_query(md).all()
    admin_findings = visible_findings_query(admin).all()
    print(f"MD visible findings count: {len(md_findings)}")
    print(f"Admin visible findings count: {len(admin_findings)}")
    assert len(md_findings) == len(all_findings), "MD should see all findings!"
    assert len(admin_findings) == len(all_findings), "Admin should see all findings!"
    print("  [PASS] MD and Admin have full organization-wide visibility across all teams.")

print("\n==========================================================")
print("ALL CRITICAL / CAPA VISIBILITY TESTS PASSED (100%)!")
print("==========================================================")
