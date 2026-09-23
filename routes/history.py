from flask import render_template, request
from flask_login import login_required, current_user
from extensions import cache
from cache_utils import per_user_cache_key
from services.history_service import get_user_history_rows


def register_history_routes(app):
    """Register /my_history route on the Flask app."""
    @app.route('/my_history')
    @login_required
    @cache.cached(timeout=300, key_prefix=per_user_cache_key)
    def my_history():
        start = request.args.get('start') or ''
        end = request.args.get('end') or ''
        form_query = request.args.get('form') or ''
        category = request.args.get('category') or 'all'
        search_query = request.args.get('q') or ''

        result = get_user_history_rows(
            user_id=current_user.user_id,
            start=start,
            end=end,
            form_query=form_query,
            category=category,
            search_query=search_query
        )

        return render_template(
            'my_history.html',
            rows=result['rows'],
            total_count=result['total_count'],
            forms_count=result['forms_count'],
            capa_count=result['capa_count'],
            form_choices=result['form_choices'],
            start=start,
            end=end,
            form_query=form_query,
            category=category,
            search_query=search_query
        )
