from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import cache
from cache_utils import per_user_cache_key
from services.dashboard_service import build_dashboard_context, get_main_dashboard_data
from services.dashboard.common import get_authorized_dashboard_teams

md_dashboard_bp = Blueprint('md_dashboard', __name__)

@md_dashboard_bp.route('/md/dashboard')
@md_dashboard_bp.route('/lead/dashboard')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def md_dashboard():
    if not (current_user.role == 'MD' or getattr(current_user, 'is_team_lead', False)):
        flash('Access denied. MD or Team Lead privileges required.', 'error')
        return redirect(url_for('dashboard'))

    selected_team = request.args.get('team')
    selected_date = request.args.get('date')

    context = build_dashboard_context(current_user, selected_team, selected_date)
    return render_template('md_dashboard.html', **context)

def register_dashboard_routes(app):
    """Register the main /dashboard route on the Flask app."""
    @app.route('/dashboard')
    @login_required
    @cache.cached(timeout=300, key_prefix=per_user_cache_key)
    def dashboard():
        data = get_main_dashboard_data(current_user)
        if data['type'] == 'render':
            return render_template(data['template'], **data['context'])
        elif data['type'] == 'redirect':
            return redirect(url_for(data['endpoint'], **data.get('params', {})))
        return redirect(url_for('login'))

