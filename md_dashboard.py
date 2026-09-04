# md_dashboard.py
# Backwards-compatibility wrapper re-exporting from routes.dashboard_routes and services.dashboard

from routes.dashboard_routes import md_dashboard_bp, md_dashboard, register_dashboard_routes
from services.dashboard.common import get_authorized_dashboard_teams
from services.dashboard_service import build_dashboard_context

__all__ = [
    'md_dashboard_bp',
    'md_dashboard',
    'register_dashboard_routes',
    'get_authorized_dashboard_teams',
    'build_dashboard_context'
]

