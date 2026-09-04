from flask import Blueprint, redirect, url_for, flash, request, send_file
from flask_login import login_required, current_user
from extensions import cache
from cache_utils import per_user_cache_key
from services.report_service import generate_pdf_report

report_bp = Blueprint('report', __name__)

@report_bp.route('/generate-report')
@cache.cached(timeout=300, key_prefix=per_user_cache_key)
@login_required
def generate_report():
    if current_user.role not in ['Admin', 'MD']:
        flash('Access denied. Only Admin and MD can generate reports.', 'danger')
        return redirect(url_for('dashboard'))

    buffer = generate_pdf_report(current_user, request.args)
    return send_file(
        buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='detailed_issue_report.pdf'
    )
