# actions.py
# Backwards-compatibility wrapper re-exporting from routes.action_routes
from routes.action_routes import actions_bp, action_home, create_action, finish_action, loop_action
from services.action_service import (
    sort_actions_group,
    build_action_tree,
    flatten_action_tree,
    prepare_actions_dashboard
)

__all__ = [
    'actions_bp', 'action_home', 'create_action', 'finish_action', 'loop_action',
    'sort_actions_group', 'build_action_tree', 'flatten_action_tree', 'prepare_actions_dashboard'
]