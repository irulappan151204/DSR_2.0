from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from extensions import cache
from cache_utils import per_user_cache_key
from services.statistics_service import get_statistics_context

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def view_statistics():
    """Render the statistics dashboard showing aggregated issue nature metrics

    across all teams (for MD) or specific team (for Team Leads).
    """
    context = get_statistics_context(current_user, request.args)
    if context is None:
        flash('Access denied. Only MD and Team Leads can view statistics.', 'danger')
        return redirect(url_for('dashboard'))

    return render_template('statistics.html', **context)
