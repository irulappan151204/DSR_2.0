# pyrefly: ignore [missing-import]
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_migrate import Migrate
from dotenv import load_dotenv

from config import Config
from extensions import db, login_manager, bcrypt, socketio, cache
from cache_utils import per_user_cache_key
from commands import create_admin_command
from utils.filters import json_escape
from models import User, Team, Issue, Action
from critical import pending_critical_count as critical_pending_count

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
socketio.init_app(app)
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

@app.template_filter('ist_strftime')
def ist_strftime_filter(date, format_string):
    """Format date in IST using format_string similar to strftime."""
    if date is None:
        return ''
    try:
        if date.tzinfo is None:
            date = date.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
        ist_date = date.astimezone(ZoneInfo("Asia/Kolkata"))
        return ist_date.strftime(format_string)
    except Exception:
        return str(date)

# Context processors
@app.context_processor
def inject_pending_actions():
    """Inject pending actions status into all templates"""
    if current_user.is_authenticated:
        now = datetime.now(ZoneInfo('Asia/Kolkata'))
        start_date_obj = datetime.strptime('2025-07-01', '%Y-%m-%d').date()
        end_date_obj = now.date()
        date_filter = db.and_(
            db.func.date(Action.created_at) >= start_date_obj,
            db.func.date(Action.created_at) <= end_date_obj
        )

        base_q = Action.query.filter(
            Action.parent_action_id.is_(None),
            Action.status != 'Finished',
            date_filter
        )

        if current_user.role == 'MD':
            pending_actions = base_q.count()
        elif current_user.is_team_lead:
            team_user_ids = [r[0] for r in db.session.query(User.user_id).filter_by(team_id=current_user.team_id).all()]
            pending_actions = base_q.filter(
                (Action.assigned_user_id.in_(team_user_ids)) |
                (Action.created_by.in_(team_user_ids))
            ).count()
        else:
            pending_actions = base_q.filter(
                (Action.assigned_user_id == current_user.user_id) |
                (Action.created_by == current_user.user_id)
            ).count()

        return {
            'has_pending_actions': pending_actions > 0,
            'pending_actions_count': pending_actions
        }
    return {
        'has_pending_actions': False,
        'pending_actions_count': 0
    }

@app.context_processor
def inject_pending_critical():
    """Inject the Critical/CAPA pending count into all templates."""
    if not current_user.is_authenticated:
        return {
            'has_pending_critical': False,
            'pending_critical_count': 0,
            'can_view_critical': False
        }

    pending = critical_pending_count(current_user)
    return {
        'has_pending_critical': pending > 0,
        'pending_critical_count': pending,
        'can_view_critical': True
    }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def ensure_default_teams():
    team1 = Team.query.filter_by(team_name='Team 1').first()
    if not team1:
        team1 = Team(team_name='Team 1')
        db.session.add(team1)

    team2 = Team.query.filter_by(team_name='Team 2').first()
    if not team2:
        team2 = Team(team_name='Team 2')
        db.session.add(team2)

    team3 = Team.query.filter_by(team_name='Team 3').first()
    if not team3:
        team3 = Team(team_name='Team 3')
        db.session.add(team3)

    db.session.commit()

@app.route('/dashboard')
@login_required
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
def dashboard():
    if current_user.role == 'Admin':
        ensure_default_teams()
        users = User.query.all()
        teams = Team.query.all()
        total_issues = Issue.query.count()
        open_issues = Issue.query.filter_by(status='Open').count()
        recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(5).all()
        return render_template('admin_dashboard.html',
                             users=users,
                             teams=teams,
                             total_issues=total_issues,
                             open_issues=open_issues,
                             recent_issues=recent_issues)
    elif current_user.role == 'Team Lead':
        team_param = 'team1' if current_user.team_id == 1 else 'team2' if current_user.team_id == 2 else 'team3'
        return redirect(url_for('md_dashboard.md_dashboard', team=team_param))
    elif current_user.role == 'Team Member':
        team_issues = Issue.query.filter_by(team_id=current_user.team_id).all()
        total_issues = len(team_issues)
        pending_issues = len([i for i in team_issues if i.status == 'Open'])
        in_progress_issues = len([i for i in team_issues if i.status == 'In Progress'])
        solved_issues = len([i for i in team_issues if i.status == 'Solved'])
        recent_issues = Issue.query.filter_by(team_id=current_user.team_id).order_by(Issue.created_at.desc()).limit(5).all()
        team = Team.query.get(current_user.team_id)
        return render_template('team_member_dashboard.html',
                             team_issues=team_issues,
                             total_issues=total_issues,
                             pending_issues=pending_issues,
                             in_progress_issues=in_progress_issues,
                             solved_issues=solved_issues,
                             recent_issues=recent_issues,
                             team=team)
    elif current_user.role == 'MD':
        users = User.query.all()
        teams = Team.query.all()
        total_issues = Issue.query.count()
        open_issues = Issue.query.filter_by(status='Open').count()
        recent_issues = Issue.query.order_by(Issue.created_at.desc()).limit(5).all()
        return render_template('md_dashboard.html',
                             users=users,
                             teams=teams,
                             total_issues=total_issues,
                             open_issues=open_issues,
                             recent_issues=recent_issues)
    return redirect(url_for('login'))

# ==========================================================================
# Register modular routes
# ==========================================================================
register_auth_routes(app)
register_admin_routes(app)
register_issues_routes(app)
register_files_routes(app)
register_history_routes(app)
register_all_form_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    socketio.run(app, debug=True)
