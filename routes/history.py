from flask import render_template, request
from flask_login import login_required, current_user
from extensions import cache
from cache_utils import per_user_cache_key
from services.history_service import get_user_history_rows

def register_history_routes(app):
    """Register /my_history route on the Flask app."""
    @app.route('/my_history')
    @cache.cached(timeout=300, key_prefix=per_user_cache_key)
    @login_required
    def my_history():
        start = request.args.get('start')
        end = request.args.get('end')
        form_query = request.args.get('form')

        history_rows = get_user_history_rows(
            user_id=current_user.user_id,
            start=start,
            end=end,
            form_query=form_query
        )

        return render_template(
            'my_history.html',
            rows=history_rows,
            start=start or '',
            end=end or '',
            form_query=form_query or ''
        )
