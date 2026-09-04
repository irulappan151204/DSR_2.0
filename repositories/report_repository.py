from extensions import db
from models import Action, User, Team, BaseForm

def get_actions_by_filters(action_filters):
    """Retrieve actions matching date filters."""
    query = Action.query
    if action_filters:
        query = query.filter(*action_filters)
    return query.all()

def get_staff_users():
    """Retrieve all users with role Member or Lead."""
    return User.query.filter(User.role.in_(['Member', 'Lead'])).all()

def get_all_users():
    """Retrieve all users."""
    return User.query.all()

def get_all_teams():
    """Retrieve all teams."""
    return Team.query.all()

def get_form_submission_counts_by_user():
    """Count submissions per user across all forms inheriting from BaseForm."""
    counts = {}
    for form_model in BaseForm.__subclasses__():
        try:
            if hasattr(form_model, 'form_id') and hasattr(form_model, 'submitted_by'):
                rows = db.session.query(form_model.form_id, form_model.submitted_by).all()
                for _, sub_by in rows:
                    if sub_by:
                        counts[sub_by] = counts.get(sub_by, 0) + 1
        except Exception:
            continue
    return counts
