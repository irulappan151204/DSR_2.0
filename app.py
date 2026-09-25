# pyrefly: ignore [missing-import]
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from sqlalchemy import text
from flask_login import current_user
from flask_migrate import Migrate
from dotenv import load_dotenv

from config import Config
from extensions import db, login_manager, bcrypt, socketio, cache, csrf, limiter
from commands import create_admin_command, sync_tables_command
from utils.filters import json_escape, ist_strftime
from models import User

# Services
from services.action_service import get_pending_actions_context
from services.capa_service import get_pending_critical_context
from services.notes_service import get_pending_reminders_context

# Blueprints
from statistics_routes import statistics_bp
from md_dashboard import md_dashboard_bp
from report_routes import report_bp
from actions import actions_bp
from acknowledgements import acknowledgements_bp
from critical import critical_bp
from routes.notes import notes_bp

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

# Configure structured logging (Issue #11)
os.makedirs('logs', exist_ok=True)
file_handler = RotatingFileHandler('logs/app.log', maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt.init_app(app)
csrf.init_app(app)
limiter.init_app(app)

# SocketIO Security: Allow origin whitelist via env var (defaults to '*' in dev)
cors_env = os.getenv('SOCKETIO_CORS_ALLOWED_ORIGINS', '*').strip()
if cors_env == '*' or not cors_env:
    cors_allowed_origins = '*'
else:
    cors_allowed_origins = [orig.strip() for orig in cors_env.split(',') if orig.strip()]

socketio_async_mode = os.getenv('SOCKETIO_ASYNC_MODE', 'threading')
socketio.init_app(app, cors_allowed_origins=cors_allowed_origins, async_mode=socketio_async_mode)
migrate = Migrate(app, db)

# Initialize cache using app.config (respects RedisCache when configured in Config)
cache.init_app(app)

# Security HTTP headers (Issues #19, #23)
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Strict-Transport-Security (HSTS) when running over HTTPS or configured for secure cookies
    if app.config.get('SESSION_COOKIE_SECURE') or app.config.get('PREFERRED_URL_SCHEME') == 'https':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Content Security Policy (Report-Only - Option A: monitors without blocking inline scripts)
    csp_policy = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://code.jquery.com; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; "
        "img-src 'self' data:; "
        "connect-src 'self' ws: wss:;"
    )
    response.headers['Content-Security-Policy-Report-Only'] = csp_policy
    return response

# Health check endpoint for container orchestration (Issues #6, #17)
@app.route('/health')
def health_check():
    """Health check endpoint for Docker and monitoring."""
    status = {"status": "healthy", "database": "unknown"}
    try:
        db.session.execute(text("SELECT 1"))
        status["database"] = "connected"
        return jsonify(status), 200
    except Exception:
        app.logger.exception("Database health check failed")
        status["status"] = "unhealthy"
        status["database"] = "disconnected"
        return jsonify(status), 503

# Register blueprints

app.register_blueprint(statistics_bp)
app.register_blueprint(md_dashboard_bp)
app.register_blueprint(report_bp)
app.register_blueprint(actions_bp)
app.register_blueprint(acknowledgements_bp)
app.register_blueprint(critical_bp)
app.register_blueprint(notes_bp)

# Register CLI commands
app.cli.add_command(create_admin_command)
app.cli.add_command(sync_tables_command)

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

@app.context_processor
def inject_pending_reminders():
    """Inject the pending Notes reminders count into all templates."""
    return get_pending_reminders_context(current_user)

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
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    socketio.run(app, debug=debug_mode)

