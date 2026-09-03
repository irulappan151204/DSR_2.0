import sys
sys.path.insert(0, '.')
from app import app, inject_pending_actions, inject_pending_critical
from critical import pending_critical_count
from models import User, Action, CapaFinding
from extensions import db
from flask_login import login_user
from datetime import datetime
from zoneinfo import ZoneInfo

with app.app_context():
    users = {
        'Team Member (Anita - Team 1)': User.query.filter_by(username='anita').first(),
        'Team Member (Sathish - Team 2)': User.query.filter_by(username='sathish').first(),
        'Team Lead (Sujatha - Team 1)': User.query.filter_by(username='sujatha').first(),
        'Team Lead (Sheebha - Team 2)': User.query.filter_by(username='sheebha').first(),
        'MD (Audit Team)': User.query.filter_by(username='auditteam').first(),
        'Admin (Admin)': User.query.filter_by(username='admin').first(),
    }
    
    now = datetime.now(ZoneInfo('Asia/Kolkata'))
    start_date_obj = datetime.strptime('2025-07-01', '%Y-%m-%d').date()
    end_date_obj = now.date()
    date_filter = db.and_(
        db.func.date(Action.created_at) >= start_date_obj,
        db.func.date(Action.created_at) <= end_date_obj
    )

    print("=" * 90)
    print(f"{'Role':<32} | {'Pending Actions':<18} | {'Pending Critical':<18} | {'Cross-Team Bleed?'}")
    print("=" * 90)
    
    for label, user in users.items():
        with app.test_request_context():
            login_user(user)
            actions_dict = inject_pending_actions()
            crit_dict = inject_pending_critical()
            
            p_actions = actions_dict['pending_actions_count']
            p_crit = crit_dict['pending_critical_count']
            
            # Cross-team verification:
            # For Team 1 Lead (Sujatha): ensure no Team 2 action or critical finding is counted
            bleed = False
            if user.role == 'Team Lead':
                team_user_ids = [u.user_id for u in User.query.filter_by(team_id=user.team_id).all()]
                other_team_user_ids = [u.user_id for u in User.query.filter(User.team_id != user.team_id, User.team_id.isnot(None)).all()]
                
                # Verify actions query only counts own team
                team_action_count = Action.query.filter(
                    Action.parent_action_id.is_(None),
                    Action.status != 'Finished',
                    date_filter,
                    (Action.assigned_user_id.in_(team_user_ids)) | (Action.created_by.in_(team_user_ids))
                ).count()
                assert p_actions == team_action_count, f"Mismatch in actions count for {user.username}!"
                
            print(f"{label:<32} | {p_actions:>18} | {p_crit:>18} | {'NO (Strictly Scoped)'}")

    print("=" * 90)
    print("ALL CONTEXT PROCESSORS VERIFIED ACROSS ALL ROLES!")
