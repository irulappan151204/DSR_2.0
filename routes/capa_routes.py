from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from extensions import db
from models import (
    User, CapaFinding,
    CAPA_STATUS_OPEN, CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_PENDING_AUDIT,
    CAPA_STATUS_REVISION_REQUIRED, CAPA_STATUS_CLOSED,
    CAPA_STATUSES, CAPA_STATUS_LABELS, CAPA_PRIORITIES,
    CAPA_DECISION_ACCEPTED, CAPA_DECISION_NOT_ACCEPTED,
    CAPA_STAGE_FINDING, CAPA_STAGE_RESPONSE, CAPA_STAGE_REVIEW,
)
from timezone_utils import now_ist
from repositories.capa_repository import (
    can_audit, get_finding_or_404, next_audit_reference,
    get_visible_findings_query, search_users_query, AUDIT_TEAM_ID
)
from services.capa_service import (
    get_audit_lookups, can_view_finding, audit_required, team_display, user_label,
    transition, log_event, store_uploads, bust_user_cache, bust_team_lead_cache,
    bust_audit_caches, _clean
)

critical_bp = Blueprint('critical', __name__, template_folder='templates/critical')

@critical_bp.route('/critical', methods=['GET'])
@login_required
def critical_home():
    status_filter = request.args.get('status') or ''
    query = get_visible_findings_query(current_user)

    counts = {status: 0 for status in CAPA_STATUSES}
    for status, total in (query.with_entities(CapaFinding.status, db.func.count(CapaFinding.form_id))
                          .group_by(CapaFinding.status).all()):
        counts[status] = total

    if status_filter in CAPA_STATUSES:
        query = query.filter(CapaFinding.status == status_filter)

    findings = query.order_by(CapaFinding.submitted_at.desc()).limit(500).all()

    return render_template(
        'critical/list.html',
        findings=findings,
        counts=counts,
        total=sum(counts.values()),
        status_filter=status_filter,
        statuses=CAPA_STATUSES,
        status_labels=CAPA_STATUS_LABELS,
        is_auditor=can_audit(current_user),
        team_display=team_display,
        user_label=user_label,
    )

@critical_bp.route('/critical/new', methods=['GET'])
@login_required
@audit_required
def new_finding():
    lookups = get_audit_lookups()
    return render_template(
        'critical/create.html',
        today=now_ist().date().isoformat(),
        next_reference=next_audit_reference(),
        is_auditor=True,
        form_data={},
        **lookups
    )

@critical_bp.route('/critical/new', methods=['POST'])
@login_required
@audit_required
def create_finding():
    title = _clean(request.form.get('title'), 255)
    description = _clean(request.form.get('description'))
    frequency = _clean(request.form.get('frequency'), 50)
    component = _clean(request.form.get('component'), 255)
    audited_by = _clean(request.form.get('audited_by'), 100)
    staff_name = _clean(request.form.get('staff_name'), 100)
    grade = _clean(request.form.get('grade'), 50)
    section = _clean(request.form.get('section'), 50)
    specification = _clean(request.form.get('specification'))
    nature_of_issue = _clean(request.form.get('nature_of_issue'), 100)
    remark = _clean(request.form.get('remark'))
    priority = _clean(request.form.get('priority'))
    recipient_raw = _clean(request.form.get('recipient_id'))
    audit_date_raw = _clean(request.form.get('audit_date'))

    recipient = User.query.get(int(recipient_raw)) if recipient_raw.isdigit() else None
    lookups = get_audit_lookups()

    form_data = {
        'title': title, 'description': description,
        'frequency': frequency, 'component': component,
        'audited_by': audited_by, 'staff_name': staff_name,
        'grade': grade, 'section': section,
        'specification': specification,
        'nature_of_issue': nature_of_issue, 'remark': remark,
        'priority': priority, 'recipient_id': recipient_raw,
        'audit_date': audit_date_raw,
        'recipient_label': user_label(recipient) if recipient else '',
    }

    def reject(message):
        flash(message, 'danger')
        return render_template(
            'critical/create.html',
            today=now_ist().date().isoformat(),
            next_reference=next_audit_reference(),
            is_auditor=True,
            form_data=form_data,
            **lookups
        ), 400

    missing = []
    if not title: missing.append('Audit Finding Title')
    if not description: missing.append('Issue Description')
    if not frequency: missing.append('Frequency')
    if not component: missing.append('Component')
    if not audited_by: missing.append('Audited By')
    if not staff_name: missing.append('Staff Name')
    if not grade: missing.append('Grade')
    if not section: missing.append('Section')
    if not specification: missing.append('Specification')
    if not nature_of_issue: missing.append('Nature of Issue / Status')
    if priority not in CAPA_PRIORITIES: missing.append('Priority')
    if recipient is None: missing.append('Recipient / Assignment')

    if missing:
        return reject(f"Please fill in all required fields: {', '.join(missing)}.")

    if recipient.user_id == current_user.user_id:
        return reject('You cannot assign a finding to yourself -- an auditor may not review their own CAPA.')

    audit_date = now_ist().date()
    if audit_date_raw:
        try:
            audit_date = datetime.strptime(audit_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return reject('Audit Date must be a valid date (YYYY-MM-DD).')

    uploads = request.files.getlist('attachments')
    owning_team_id = current_user.team_id or AUDIT_TEAM_ID

    finding = None
    for attempt in range(5):
        finding = CapaFinding(
            team_id=owning_team_id,
            submitted_by=current_user.user_id,
            audit_reference=next_audit_reference(audit_date),
            title=title,
            description=description,
            frequency=frequency,
            component=component,
            audited_by=audited_by,
            staff_name=staff_name,
            grade=grade,
            section=section,
            specification=specification,
            nature_of_issue=nature_of_issue,
            remark=remark,
            priority=priority,
            audit_date=audit_date,
            recipient_id=recipient.user_id,
            status=CAPA_STATUS_PENDING_RECIPIENT,
            revision_count=0,
        )
        db.session.add(finding)
        try:
            db.session.flush()
            break
        except IntegrityError:
            db.session.rollback()
            finding = None

    if finding is None:
        flash('Could not allocate an audit reference. Please try again.', 'danger')
        return redirect(url_for('critical.new_finding'))

    try:
        store_uploads(uploads, finding, CAPA_STAGE_FINDING, current_user)
    except ValueError as exc:
        db.session.rollback()
        return reject(str(exc))

    log_event(finding, current_user, 'FINDING_CREATED',
              None, CAPA_STATUS_PENDING_RECIPIENT,
              f'Audit finding {finding.audit_reference} created with {finding.priority} priority. Assigned to {user_label(recipient)}.')

    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        print(f'Error creating CAPA finding: {exc}')
        return reject('Failed to create the finding. Please try again.')

    bust_user_cache(recipient.user_id)
    bust_team_lead_cache(recipient.team_id)
    bust_audit_caches()
    flash(f'Finding {finding.audit_reference} created. New CAPA assigned to {recipient.username}.', 'success')
    return redirect(url_for('critical.finding_detail', finding_id=finding.form_id))

@critical_bp.route('/critical/<int:finding_id>/edit', methods=['GET'])
@login_required
@audit_required
def edit_finding(finding_id):
    finding = get_finding_or_404(finding_id)
    if finding.is_closed:
        flash('Closed findings cannot be edited.', 'warning')
        return redirect(url_for('critical.finding_detail', finding_id=finding.form_id))

    lookups = get_audit_lookups()
    form_data = {
        'title': finding.title,
        'description': finding.description,
        'frequency': finding.frequency,
        'component': finding.component,
        'audited_by': finding.audited_by,
        'staff_name': finding.staff_name,
        'grade': finding.grade,
        'section': finding.section,
        'specification': finding.specification,
        'nature_of_issue': finding.nature_of_issue,
        'remark': finding.remark,
        'priority': finding.priority,
        'audit_date': finding.audit_date.isoformat() if finding.audit_date else '',
        'recipient_id': str(finding.recipient_id),
        'recipient_label': user_label(finding.recipient),
    }

    return render_template(
        'critical/edit.html',
        finding=finding,
        form_data=form_data,
        is_auditor=True,
        **lookups
    )

@critical_bp.route('/critical/<int:finding_id>/edit', methods=['POST'])
@login_required
@audit_required
def update_finding(finding_id):
    finding = get_finding_or_404(finding_id)
    if finding.is_closed:
        flash('Closed findings cannot be edited.', 'warning')
        return redirect(url_for('critical.finding_detail', finding_id=finding.form_id))

    title = _clean(request.form.get('title'), 255)
    description = _clean(request.form.get('description'))
    frequency = _clean(request.form.get('frequency'), 50)
    component = _clean(request.form.get('component'), 255)
    audited_by = _clean(request.form.get('audited_by'), 100)
    staff_name = _clean(request.form.get('staff_name'), 100)
    grade = _clean(request.form.get('grade'), 50)
    section = _clean(request.form.get('section'), 50)
    specification = _clean(request.form.get('specification'))
    nature_of_issue = _clean(request.form.get('nature_of_issue'), 100)
    remark = _clean(request.form.get('remark'))
    priority = _clean(request.form.get('priority'))
    audit_date_raw = _clean(request.form.get('audit_date'))

    lookups = get_audit_lookups()
    form_data = {
        'title': title, 'description': description,
        'frequency': frequency, 'component': component,
        'audited_by': audited_by, 'staff_name': staff_name,
        'grade': grade, 'section': section,
        'specification': specification,
        'nature_of_issue': nature_of_issue, 'remark': remark,
        'priority': priority, 'audit_date': audit_date_raw,
        'recipient_id': str(finding.recipient_id),
        'recipient_label': user_label(finding.recipient),
    }

    def reject(msg):
        flash(msg, 'danger')
        return render_template(
            'critical/edit.html', finding=finding, form_data=form_data,
            is_auditor=True, **lookups
        ), 400

    missing = []
    if not title: missing.append('Audit Finding Title')
    if not description: missing.append('Issue Description')
    if not frequency: missing.append('Frequency')
    if not component: missing.append('Component')
    if not audited_by: missing.append('Audited By')
    if not staff_name: missing.append('Staff Name')
    if not grade: missing.append('Grade')
    if not section: missing.append('Section')
    if not specification: missing.append('Specification')
    if not nature_of_issue: missing.append('Nature of Issue / Status')
    if priority not in CAPA_PRIORITIES: missing.append('Priority')

    if missing:
        return reject(f"Please fill in all required fields: {', '.join(missing)}.")

    audit_date = finding.audit_date
    if audit_date_raw:
        try:
            audit_date = datetime.strptime(audit_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return reject('Audit Date must be a valid date (YYYY-MM-DD).')

    finding.title = title
    finding.description = description
    finding.frequency = frequency
    finding.component = component
    finding.audited_by = audited_by
    finding.staff_name = staff_name
    finding.grade = grade
    finding.section = section
    finding.specification = specification
    finding.nature_of_issue = nature_of_issue
    finding.remark = remark
    finding.priority = priority
    finding.audit_date = audit_date

    uploads = request.files.getlist('attachments')
    if uploads:
        try:
            store_uploads(uploads, finding, CAPA_STAGE_FINDING, current_user)
        except ValueError as exc:
            return reject(str(exc))

    log_event(finding, current_user, 'FINDING_UPDATED', finding.status, finding.status,
              f'Finding details updated by {current_user.username}.')

    try:
        db.session.commit()
    except Exception as exc:
        db.session.rollback()
        return reject('Failed to update finding. Please try again.')

    flash(f'Finding {finding.audit_reference} updated successfully.', 'success')
    return redirect(url_for('critical.finding_detail', finding_id=finding.form_id))

@critical_bp.route('/critical/<int:finding_id>', methods=['GET'])
@login_required
def finding_detail(finding_id):
    finding = get_finding_or_404(finding_id)
    if not can_view_finding(finding, current_user):
        flash('You are not authorized to view this CAPA finding.', 'danger')
        return redirect(url_for('critical.critical_home'))

    is_auditor = can_audit(current_user)
    is_recipient = finding.recipient_id == current_user.user_id

    can_respond = is_recipient and finding.awaiting_recipient
    can_review = is_auditor and not is_recipient and finding.awaiting_audit_review
    can_edit = is_auditor and not finding.is_closed

    return render_template(
        'critical/detail.html',
        finding=finding,
        events=finding.events,
        finding_files=finding.files_for_stage(CAPA_STAGE_FINDING),
        response_files=finding.files_for_stage(CAPA_STAGE_RESPONSE),
        review_files=finding.files_for_stage(CAPA_STAGE_REVIEW),
        is_auditor=is_auditor,
        is_recipient=is_recipient,
        can_respond=can_respond,
        can_review=can_review,
        can_edit=can_edit,
        decision_accepted=CAPA_DECISION_ACCEPTED,
        decision_not_accepted=CAPA_DECISION_NOT_ACCEPTED,
        status_labels=CAPA_STATUS_LABELS,
        team_display=team_display,
        user_label=user_label,
    )

@critical_bp.route('/critical/api/users', methods=['GET'])
@login_required
def search_users():
    if not can_audit(current_user):
        return jsonify({'error': 'Not authorized.'}), 403

    term = _clean(request.args.get('q'))
    users = search_users_query(term, current_user.user_id)
    return jsonify({'users': [{
        'user_id': u.user_id,
        'username': u.username,
        'team': team_display(u),
        'role': u.role,
        'label': user_label(u),
    } for u in users if u.user_id != current_user.user_id]})

@critical_bp.route('/critical/<int:finding_id>/respond', methods=['POST'])
@login_required
def submit_response(finding_id):
    finding = get_finding_or_404(finding_id)
    detail_url = url_for('critical.finding_detail', finding_id=finding.form_id)

    if finding.recipient_id != current_user.user_id:
        flash('Only the assigned recipient can submit a CAPA response.', 'danger')
        return redirect(url_for('critical.critical_home'))
    if not finding.awaiting_recipient:
        flash('This finding is not awaiting your response.', 'warning')
        return redirect(detail_url)

    action_taken = _clean(request.form.get('action_taken_report'))
    root_cause = _clean(request.form.get('root_cause_analysis'))
    capa_1 = _clean(request.form.get('capa_1'))

    if not action_taken or not root_cause or not capa_1:
        flash('Action Taken Report, Root Cause Analysis and CAPA 1 are all required.', 'danger')
        return redirect(detail_url)

    is_revision = finding.status == CAPA_STATUS_REVISION_REQUIRED

    finding.action_taken_report = action_taken
    finding.root_cause_analysis = root_cause
    finding.capa_1 = capa_1
    finding.capa_1_submitted_at = now_ist()
    finding.capa_1_submitted_by = current_user.user_id

    files = request.files.getlist('attachments')
    try:
        store_uploads(files, finding, CAPA_STAGE_RESPONSE, current_user)
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), 'danger')
        return redirect(detail_url)

    valid_uploads = [f for f in files if getattr(f, 'filename', '')] if files else []
    attach_count = len(valid_uploads)
    attach_msg = f' with {attach_count} attachment(s)' if attach_count > 0 else ''
    comment = (
        f'Revision {finding.revision_count} resubmitted by {current_user.username}{attach_msg}.'
        if is_revision else
        f'Action Taken Report, RCA, and CAPA 1 submitted by {current_user.username}{attach_msg}.'
    )

    try:
        transition(finding, CAPA_STATUS_PENDING_AUDIT, current_user,
                   'CAPA_RESUBMITTED' if is_revision else 'CAPA_RESPONSE_SUBMITTED',
                   comment)
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), 'danger')
        return redirect(detail_url)
    except Exception as exc:
        db.session.rollback()
        print(f'Error submitting CAPA response: {exc}')
        flash('Failed to submit the CAPA response. Please try again.', 'danger')
        return redirect(detail_url)

    bust_user_cache(current_user.user_id)
    bust_team_lead_cache(current_user.team_id)
    bust_audit_caches()
    flash(f'CAPA response submitted for Audit Reference {finding.audit_reference}.', 'success')
    return redirect(detail_url)

@critical_bp.route('/critical/<int:finding_id>/review', methods=['POST'])
@login_required
@audit_required
def submit_review(finding_id):
    finding = get_finding_or_404(finding_id)
    detail_url = url_for('critical.finding_detail', finding_id=finding.form_id)

    if finding.recipient_id == current_user.user_id:
        flash('You cannot review a CAPA that is assigned to you.', 'danger')
        return redirect(detail_url)
    if not finding.awaiting_audit_review:
        flash('This finding is not awaiting audit review.', 'warning')
        return redirect(detail_url)

    capa_2 = _clean(request.form.get('capa_2'))
    decision = _clean(request.form.get('audit_decision')).upper()
    justification = _clean(request.form.get('audit_justification'))

    if not capa_2:
        flash('CAPA 2 is required.', 'danger')
        return redirect(detail_url)
    if decision not in (CAPA_DECISION_ACCEPTED, CAPA_DECISION_NOT_ACCEPTED):
        flash('Select an audit decision: Accepted or Not Accepted.', 'danger')
        return redirect(detail_url)
    if decision == CAPA_DECISION_NOT_ACCEPTED and not justification:
        flash('Justification is mandatory when the CAPA is not accepted.', 'danger')
        return redirect(detail_url)

    reviewed_at = now_ist()
    finding.capa_2 = capa_2
    finding.capa_2_submitted_at = reviewed_at
    finding.capa_2_submitted_by = current_user.user_id
    finding.audit_decision = decision
    finding.audit_justification = justification if decision == CAPA_DECISION_NOT_ACCEPTED else None
    finding.audit_reviewed_by = current_user.user_id
    finding.audit_reviewed_at = reviewed_at

    try:
        store_uploads(request.files.getlist('attachments'), finding,
                      CAPA_STAGE_REVIEW, current_user)
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), 'danger')
        return redirect(detail_url)

    try:
        if decision == CAPA_DECISION_ACCEPTED:
            finding.closed_at = reviewed_at
            transition(finding, CAPA_STATUS_CLOSED, current_user, 'CAPA_ACCEPTED',
                       f'CAPA 2 entered and accepted by auditor {current_user.username}. Finding closed.')
            message = f'CAPA accepted and issue closed for {finding.audit_reference}.'
        else:
            finding.closed_at = None
            finding.revision_count = (finding.revision_count or 0) + 1
            justification_text = f' Justification: {justification}' if justification else ''
            transition(finding, CAPA_STATUS_REVISION_REQUIRED, current_user,
                       'CAPA_REVISION_REQUESTED',
                       f'Revision {finding.revision_count} requested by auditor {current_user.username}.{justification_text}')
            message = (f'CAPA revision required -- {finding.audit_reference} returned to {finding.recipient.username}.')
        db.session.commit()
    except ValueError as exc:
        db.session.rollback()
        flash(str(exc), 'danger')
        return redirect(detail_url)
    except Exception as exc:
        db.session.rollback()
        print(f'Error submitting CAPA review: {exc}')
        flash('Failed to submit the audit review. Please try again.', 'danger')
        return redirect(detail_url)

    bust_user_cache(finding.recipient_id)
    bust_team_lead_cache(finding.recipient.team_id)
    bust_audit_caches()
    flash(message, 'success')
    return redirect(detail_url)
