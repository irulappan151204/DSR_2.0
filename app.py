# pyrefly: ignore [missing-import]
import os
from flask import Flask
from flask_login import current_user
from flask_migrate import Migrate
from dotenv import load_dotenv

from config import Config
from extensions import db, login_manager, bcrypt, socketio, cache
from commands import create_admin_command
from utils.filters import json_escape, ist_strftime
from models import User

# Services
from services.action_service import get_pending_actions_context
from services.capa_service import get_pending_critical_context

# Blueprints
from statistics_routes import statistics_bp
from md_dashboard import md_dashboard_bp
from report_routes import report_bp
from actions import actions_bp
from acknowledgements import acknowledgements_bp
from critical import critical_bp

# Domain route registration functions
from routes.auth import register_auth_routes
from routes.admin import register_admin_routes
from routes.issues import register_issues_routes
from routes.files import register_files_routes
from routes.history import register_history_routes
from routes.forms import register_all_form_routes
from routes.dashboard_routes import register_dashboard_routes

# Load environment variables
load_dotenv()
os.environ['FLASK_APP'] = 'app.py'

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt.init_app(app)
socketio.init_app(app, cors_allowed_origins="*", async_mode='threading')
migrate = Migrate(app, db)

# Configure cache
cache_config = {
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 300,
    'CACHE_KEY_PREFIX': 'qmis_',
    'CACHE_THRESHOLD': 1000,
}
cache.init_app(app, config=cache_config)

# Register blueprints
app.register_blueprint(statistics_bp)
app.register_blueprint(md_dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(acknowledgements_bp)
app.register_blueprint(critical_bp)

# Register CLI commands
app.cli.add_command(create_admin_command)

# Custom Jinja2 filters
app.template_filter('json_escape')(json_escape)
app.template_filter('ist_strftime')(ist_strftime)

# Context processors
@app.context_processor
def inject_pending_actions():
    """Inject pending actions status into all templates."""
    return get_pending_actions_context(current_user)

@app.context_processor
def inject_pending_critical():
    """Inject the Critical/CAPA pending count into all templates."""
    return get_pending_critical_context(current_user)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================================================
# Register modular routes
# ==========================================================================
register_auth_routes(app)
register_admin_routes(app)
register_issues_routes(app)
register_files_routes(app)
register_history_routes(app)
register_all_form_routes(app)
register_dashboard_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
