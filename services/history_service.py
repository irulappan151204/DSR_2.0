import re
from datetime import datetime, timedelta, date, time
from flask import url_for
from models import CAPA_STATUS_LABELS
from repositories.history_repository import (
    get_model_meta,
    get_form_choices,
    fetch_capa_history,
    fetch_form_history
)


def _clean_field_label(col_name):
    """Convert raw database column names into human-readable labels."""
    label = col_name
    # Common suffixes
    label = re.sub(r'_jr$', ' (Jr. School)', label)
    label = re.sub(r'_sr$', ' (Senior School)', label)
    label = re.sub(r'_paid$', ' (Paid)', label)
    label = re.sub(r'_reg$', ' (Regular)', label)
    label = re.sub(r'_pct$', ' %', label)
    label = re.sub(r'_status$', ' Status', label)
    label = re.sub(r'_desc$', ' Description', label)

    # Replace remaining underscores and title case
    parts = label.split(' ')
    clean_parts = []
    for part in parts:
        if part.startswith('('):
            clean_parts.append(part)
        else:
            clean_parts.append(part.replace('_', ' ').title())
    return ' '.join(clean_parts).replace('  ', ' ')


def _format_value(val, col_name=''):
    """Safely format database column values for user display."""
    if val is None or val == '':
        return None
    if isinstance(val, bool):
        return 'Yes' if val else 'No'
    if isinstance(val, (datetime, date)):
        return val.strftime('%b %d, %Y') if isinstance(val, date) and not isinstance(val, datetime) else val.strftime('%b %d, %Y %I:%M %p')
    if isinstance(val, time):
        return val.strftime('%I:%M %p')
    if isinstance(val, float):
        if 'pct' in col_name.lower() or 'percent' in col_name.lower():
            return f"{val:.1f}%"
        return f"{val:.2f}"
    return str(val).strip()


def serialize_form_record(record, model_name):
    """Safely serialize an operational form model instance into clean display data.
    
    CRITICAL: Never inspects dir(record) or ORM relationships to prevent
    bound methods or registry pointers from leaking into the UI.
    """
    meta = get_model_meta(model_name)
    data_fields = {}

    excluded_cols = {
        'form_id', 'team_id', 'submitted_by', 'submitted_at',
        'media_file_id', 'finding_id', 'query', 'metadata'
    }

    # Iterate strictly over real database table columns
    if hasattr(record, '__table__'):
        for col in record.__table__.columns:
            if col.name in excluded_cols:
                continue
            raw_val = getattr(record, col.name, None)
            formatted = _format_value(raw_val, col.name)
            if formatted:
                label = _clean_field_label(col.name)
                data_fields[label] = formatted

    return {
        'type': 'form',
        'category': meta['dept_name'],
        'badge_class': meta['badge'],
        'reference': f"REF-#{record.form_id}",
        'title': meta['title'],
        'form_key': model_name,
        'form_id': record.form_id,
        'submitted_at': record.submitted_at,
        'status': 'Submitted',
        'status_label': 'Submitted',
        'status_css': 'capa-closed',
        'user_relation': 'Submitter',
        'detail_url': None,
        'data_fields': data_fields
    }


def serialize_capa_record(record, user_id):
    """Serialize a CAPA audit finding with rich workflow metadata and safe fields."""
    status_label = CAPA_STATUS_LABELS.get(record.status, record.status.replace('_', ' ').title())
    status_css = getattr(record, 'status_css', 'capa-pending-recipient')

    # Determine user's role in this finding
    if record.recipient_id == user_id:
        relation = 'Assigned Recipient'
    elif record.submitted_by == user_id:
        relation = 'Auditor / Creator'
    elif record.capa_1_submitted_by == user_id:
        relation = 'CAPA 1 Author'
    elif record.capa_2_submitted_by == user_id:
        relation = 'CAPA 2 Author'
    else:
        relation = 'Participant'

    # Build clean observation and response fieldset
    data_fields = {}
    if record.audit_reference: data_fields['Audit Reference'] = record.audit_reference
    if record.audit_date: data_fields['Audit Date'] = record.audit_date.strftime('%b %d, %Y')
    if record.component: data_fields['Component'] = record.component
    if record.audited_by: data_fields['Audited By'] = record.audited_by
    if record.staff_name: data_fields['Staff Name'] = record.staff_name
    
    grade_sec = f"{record.grade or ''} {record.section or ''}".strip()
    if grade_sec: data_fields['Grade / Section'] = grade_sec
    
    if record.specification: data_fields['Specification'] = record.specification
    if record.nature_of_issue: data_fields['Nature of Issue'] = record.nature_of_issue
    if record.priority: data_fields['Priority'] = record.priority
    if record.description: data_fields['Description'] = record.description
    if record.remark: data_fields['Remark'] = record.remark

    # CAPA Responses (if present)
    if record.action_taken_report: data_fields['Action Taken Report'] = record.action_taken_report
    if record.root_cause_analysis: data_fields['Root Cause Analysis'] = record.root_cause_analysis
    if record.capa_1: data_fields['CAPA 1 (Corrective Action)'] = record.capa_1
    if record.capa_2: data_fields['CAPA 2 (Preventive Action)'] = record.capa_2
    if record.audit_decision: data_fields['Audit Decision'] = record.audit_decision
    if record.audit_justification: data_fields['Audit Justification'] = record.audit_justification

    detail_url = None
    try:
        detail_url = url_for('critical.finding_detail', finding_id=record.form_id)
    except Exception:
        pass

    return {
        'type': 'capa',
        'category': 'Quality Audit & CAPA',
        'badge_class': 'badge-capa',
        'reference': record.audit_reference or f"AUD-#{record.form_id}",
        'title': record.title,
        'form_key': 'CapaFinding',
        'form_id': record.form_id,
        'submitted_at': record.submitted_at,
        'status': record.status,
        'status_label': status_label,
        'status_css': status_css,
        'user_relation': relation,
        'priority': record.priority,
        'detail_url': detail_url,
        'data_fields': data_fields
    }


def get_user_history_rows(user_id, start=None, end=None, form_query=None, category='all', search_query=None):
    """Fetch, filter, and construct clean historical activity records for a user."""
    start_dt = None
    end_dt = None
    try:
        if start:
            start_dt = datetime.strptime(start, '%Y-%m-%d')
        if end:
            end_dt = datetime.strptime(end, '%Y-%m-%d') + timedelta(days=1)
    except Exception:
        start_dt = None
        end_dt = None

    history_rows = []
    category = (category or 'all').lower().strip()

    # 1. Fetch CAPA Findings if requested
    if category in ('all', 'capa') and (not form_query or form_query == 'CapaFinding'):
        capa_records = fetch_capa_history(user_id, start_dt, end_dt)
        for cr in capa_records:
            history_rows.append(serialize_capa_record(cr, user_id))

    # 2. Fetch Operational Form Submissions if requested
    if category in ('all', 'forms') and form_query != 'CapaFinding':
        form_results = fetch_form_history(user_id, start_dt, end_dt, form_query)
        for model_name, records in form_results:
            for r in records:
                history_rows.append(serialize_form_record(r, model_name))

    # 3. Apply keyword search filter across reference, title, or field values if provided
    if search_query:
        sq = search_query.lower().strip()
        filtered = []
        for row in history_rows:
            matched = (
                sq in row['reference'].lower() or
                sq in row['title'].lower() or
                sq in row.get('status_label', '').lower() or
                any(sq in k.lower() or sq in str(v).lower() for k, v in row['data_fields'].items())
            )
            if matched:
                filtered.append(row)
        history_rows = filtered

    # 4. Sort overall records chronologically (newest first)
    history_rows.sort(key=lambda x: x['submitted_at'] if x['submitted_at'] else datetime.min, reverse=True)

    # 5. Compute summary statistics
    total_count = len(history_rows)
    forms_count = sum(1 for r in history_rows if r['type'] == 'form')
    capa_count = sum(1 for r in history_rows if r['type'] == 'capa')

    return {
        'rows': history_rows,
        'total_count': total_count,
        'forms_count': forms_count,
        'capa_count': capa_count,
        'form_choices': get_form_choices()
    }
