from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict
from sqlalchemy.orm.attributes import set_committed_value
from extensions import db
from models import Action, User
from repositories.action_repository import (
    get_assignable_users,
    get_actions_query_for_user,
    get_all_teams
)

def sort_actions_group(action_list):
    """Sort actions: unfinished first (by created_at desc), then finished (by completed_at desc, then created_at desc)."""
    unfinished = [a for a in action_list if a.status != 'Finished']
    finished = [a for a in action_list if a.status == 'Finished']
    unfinished_sorted = sorted(unfinished, key=lambda a: a.created_at, reverse=True)
    finished_sorted = sorted(finished, key=lambda a: (a.completed_at or datetime.min, a.created_at), reverse=True)
    return unfinished_sorted + finished_sorted

def build_action_tree(actions_list):
    """Build a hierarchical tree structure for actions without N+1 queries using set_committed_value."""
    parent_actions = [a for a in actions_list if a.parent_action_id is None]
    child_actions = [a for a in actions_list if a.parent_action_id is not None]

    children_by_parent = defaultdict(list)
    for child in child_actions:
        children_by_parent[child.parent_action_id].append(child)

    parent_actions_sorted = sort_actions_group(parent_actions)

    def build_children_for_parent(parent):
        if parent.id in children_by_parent:
            children = sort_actions_group(children_by_parent[parent.id])
            for child in children:
                child_nested = build_children_for_parent(child)
                set_committed_value(child, 'child_actions', child_nested)
            return children
        else:
            return []

    for parent in parent_actions_sorted:
        children = build_children_for_parent(parent)
        set_committed_value(parent, 'child_actions', children)

    for a in actions_list:
        if 'child_actions' not in a.__dict__:
            set_committed_value(a, 'child_actions', [])

    return parent_actions_sorted

def flatten_action_tree(parent_list):
    """Flatten tree structure into a list while maintaining hierarchy."""
    result = []
    for parent in parent_list:
        result.append(parent)
        if hasattr(parent, 'child_actions') and parent.child_actions:
            result.extend(flatten_action_tree(parent.child_actions))
    return result

def get_ordered_action_hierarchy(actions):
    """Build hierarchy and return flat list preserving parent-child adjacency."""
    parent_actions = build_action_tree(actions)
    ordered_actions = flatten_action_tree(parent_actions)

    all_parent_ids = set()
    def collect_parent_ids(parent_list):
        for parent in parent_list:
            all_parent_ids.add(parent.id)
            if hasattr(parent, 'child_actions') and parent.child_actions:
                collect_parent_ids(parent.child_actions)
    collect_parent_ids(parent_actions)

    orphan_children = [a for a in actions if a.parent_action_id is not None and a.parent_action_id not in all_parent_ids]
    if orphan_children:
        ordered_actions.extend(sort_actions_group(orphan_children))

    return ordered_actions

def prepare_actions_dashboard(user, filter_date, start_date, end_date):
    """Orchestrate action querying, status decoration, hierarchy building, and count calculation."""
    now = datetime.now(ZoneInfo('Asia/Kolkata'))

    if not filter_date and not start_date and not end_date:
        start_date = '2025-07-01'
        end_date = now.date().strftime('%Y-%m-%d')

    date_filter = None
    if filter_date:
        try:
            filter_date_obj = datetime.strptime(filter_date, '%Y-%m-%d').date()
            date_filter = db.func.date(Action.created_at) == filter_date_obj
        except ValueError:
            filter_date = None
    elif start_date and end_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            date_filter = db.and_(
                db.func.date(Action.created_at) >= start_date_obj,
                db.func.date(Action.created_at) <= end_date_obj
            )
        except ValueError:
            start_date = None
            end_date = None

    users = get_assignable_users(user)
    actions = get_actions_query_for_user(user, date_filter)
    has_pending_actions = any(a.status != 'Finished' for a in actions)

    # Decorate overdue & finished statuses
    for action in actions:
        due_date = action.due_date
        if due_date is not None and due_date.tzinfo is None:
            due_date = due_date.replace(tzinfo=ZoneInfo('Asia/Kolkata'))
        action.is_overdue = (action.status != 'Finished' and due_date < now)
        action.is_finished = (action.status == 'Finished')

    # MD Team Action counts
    team_action_counts = None
    if user.role == 'MD':
        teams = get_all_teams()
        team_action_counts = {}
        team_display_names = {
            'Team 1': 'Academic',
            'Team 2': 'Admin', 
            'Team 3': 'Audit'
        }
        for team in teams:
            team_user_set = set(u.user_id for u in users if u.team_id == team.team_id)
            display_name = team_display_names.get(team.team_name, team.team_name)

            t_parents = [a for a in actions if a.parent_action_id is None and (a.assigned_user_id in team_user_set or a.created_by in team_user_set)]
            t_children = [a for a in actions if a.parent_action_id is not None and (a.assigned_user_id in team_user_set or a.created_by in team_user_set)]

            team_action_counts[display_name] = {
                'total': len(t_parents),
                'completed': sum(1 for a in t_parents if a.status == 'Finished'),
                'pending': sum(1 for a in t_parents if a.status != 'Finished'),
                'overdue': sum(1 for a in t_parents if a.is_overdue),
                'followup': len(t_children),
                'priority': {p: sum(1 for a in t_parents if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
            }

    actions = get_ordered_action_hierarchy(actions)

    # In-memory counts calculation
    parent_actions_list = [a for a in actions if a.parent_action_id is None]
    child_actions_list = [a for a in actions if a.parent_action_id is not None]

    if user.role in ['MD', 'Team Lead']:
        action_counts = {
            'parent': {
                'total': len(parent_actions_list),
                'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
            },
            'child': {
                'total': len(child_actions_list),
                'completed': sum(1 for a in child_actions_list if a.status == 'Finished'),
                'pending': sum(1 for a in child_actions_list if a.status != 'Finished'),
                'overdue': sum(1 for a in child_actions_list if a.is_overdue)
            }
        }
        priority_counts = {
            'parent': {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']},
            'child': {p: sum(1 for a in child_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}
        }
    else:
        # Admin or Team Member
        action_counts = {
            'total': len(parent_actions_list),
            'completed': sum(1 for a in parent_actions_list if a.status == 'Finished'),
            'pending': sum(1 for a in parent_actions_list if a.status != 'Finished'),
            'overdue': sum(1 for a in parent_actions_list if a.is_overdue)
        }
        priority_counts = {p: sum(1 for a in parent_actions_list if a.priority == p) for p in ['Critical', 'High', 'Medium', 'Low']}

    return {
        'users': users,
        'actions': actions,
        'action_counts': action_counts,
        'priority_counts': priority_counts,
        'team_action_counts': team_action_counts,
        'has_pending_actions': has_pending_actions,
        'filter_date': filter_date,
        'start_date': start_date,
        'end_date': end_date
    }
