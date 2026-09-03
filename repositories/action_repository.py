from extensions import db
from models import Action, User, Team
from sqlalchemy.orm import joinedload

def get_action_by_id(action_id):
    """Retrieve an Action by ID or None."""
    return Action.query.get(action_id)

def get_action_or_404(action_id):
    """Retrieve an Action by ID or raise 404."""
    return Action.query.get_or_404(action_id)

def get_assignable_users(user):
    """Fetch users available for action assignment based on caller role."""
    if user.role == 'MD':
        return User.query.all()
    elif user.is_team_lead:
        return User.query.all()
    else:
        return User.query.filter_by(team_id=user.team_id).all()

def get_actions_query_for_user(user, date_filter=None):
    """Retrieve all actions (parent + child) relevant to the given user."""
    if user.role == 'MD':
        base_query = Action.query.options(joinedload(Action.assigned_user))
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        return base_query.all()

    elif user.is_team_lead:
        team_user_ids = [u.user_id for u in User.query.filter_by(team_id=user.team_id).all()]
        base_query = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id.in_(team_user_ids)) |
            (Action.created_by.in_(team_user_ids)) |
            (Action.assigned_user_id == user.user_id) |
            (Action.created_by == user.user_id)
        )
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        actions = base_query.all()

        child_actions = Action.query.options(joinedload(Action.assigned_user)).filter(
            ((Action.assigned_user_id.in_(team_user_ids)) | (Action.assigned_user_id == user.user_id)) & 
            (Action.parent_action_id != None)
        )
        if date_filter is not None:
            child_actions = child_actions.filter(date_filter)
        child_actions = child_actions.all()

        parent_ids = set(ca.parent_action_id for ca in child_actions if ca.parent_action_id)
        if parent_ids:
            parent_actions = Action.query.options(joinedload(Action.assigned_user)).filter(Action.id.in_(parent_ids))
            if date_filter is not None:
                parent_actions = parent_actions.filter(date_filter)
            parent_actions = parent_actions.all()

            action_ids = set(a.id for a in actions)
            for pa in parent_actions:
                if pa.id not in action_ids:
                    actions.append(pa)
                    action_ids.add(pa.id)

        return actions

    else:
        # Team Member
        base_query = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id == user.user_id) |
            (Action.created_by == user.user_id)
        )
        if date_filter is not None:
            base_query = base_query.filter(date_filter)
        actions = base_query.all()

        child_actions = Action.query.options(joinedload(Action.assigned_user)).filter(
            (Action.assigned_user_id == user.user_id) & (Action.parent_action_id != None)
        )
        if date_filter is not None:
            child_actions = child_actions.filter(date_filter)
        child_actions = child_actions.all()

        parent_ids = set(ca.parent_action_id for ca in child_actions if ca.parent_action_id)
        if parent_ids:
            parent_actions = Action.query.options(joinedload(Action.assigned_user)).filter(Action.id.in_(parent_ids))
            if date_filter is not None:
                parent_actions = parent_actions.filter(date_filter)
            parent_actions = parent_actions.all()

            action_ids = set(a.id for a in actions)
            for pa in parent_actions:
                if pa.id not in action_ids:
                    actions.append(pa)
                    action_ids.add(pa.id)

        return actions

def get_all_teams():
    return Team.query.all()
