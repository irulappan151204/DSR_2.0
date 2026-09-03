# routes/__init__.py
from .auth import register_auth_routes
from .admin import register_admin_routes
from .issues import register_issues_routes
from .files import register_files_routes
from .history import register_history_routes
from .forms import register_all_form_routes
