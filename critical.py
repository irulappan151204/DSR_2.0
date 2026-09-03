"""Critical / CAPA workflow.

Audit (Team 3) creates a finding -> a recipient drawn from the users table
submits an Action Taken Report, Root Cause Analysis and CAPA 1 -> Audit reviews,
adds CAPA 2 and either accepts (closing the finding) or rejects with a mandatory
justification, which returns the CAPA to the recipient for revision.

Every status change goes through _transition(), the only writer of
CapaFinding.status, which always appends a CapaEvent row for the audit trail.
"""
from datetime import datetime
from functools import wraps

from flask import (Blueprint, render_template, request, redirect, url_for,
                   flash, jsonify)
from flask_login import login_required, current_user
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from extensions import db, cache
from models import (
    User, Team, FileStorage, CapaFinding, CapaEvent, CapaAttachment,
    CAPA_STATUS_OPEN, CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_PENDING_AUDIT,
    CAPA_STATUS_REVISION_REQUIRED, CAPA_STATUS_CLOSED,
    CAPA_STATUSES, CAPA_STATUS_LABELS, CAPA_PRIORITIES,
    CAPA_DECISION_ACCEPTED, CAPA_DECISION_NOT_ACCEPTED,
    CAPA_STAGE_FINDING, CAPA_STAGE_RESPONSE, CAPA_STAGE_REVIEW,
)
from timezone_utils import now_ist

critical_bp = Blueprint('critical', __name__, template_folder='templates/critical')

# Same 200MB ceiling the existing DSR upload endpoints enforce.
MAX_UPLOAD_BYTES = 200 * 1024 * 1024

# Display names used in actions.py and the dashboards.
TEAM_DISPLAY_NAMES = {'Team 1': 'Academic', 'Team 2': 'Admin', 'Team 3': 'Audit'}

# The audit team is team_id 3, but the production `auditteam` account is a
# role='MD' user with team_id=NULL and no team has a lead assigned -- a bare
# team_id check would lock the real auditors out. Permission is a predicate.
AUDIT_TEAM_ID = 3
AUDIT_ROLES = ('MD', 'Admin')

# Legal status transitions. Anything not listed here is refused server-side.
ALLOWED_TRANSITIONS = {
    CAPA_STATUS_OPEN: {CAPA_STATUS_PENDING_RECIPIENT},
    CAPA_STATUS_PENDING_RECIPIENT: {CAPA_STATUS_PENDING_AUDIT},
    CAPA_STATUS_PENDING_AUDIT: {CAPA_STATUS_CLOSED, CAPA_STATUS_REVISION_REQUIRED},
    CAPA_STATUS_REVISION_REQUIRED: {CAPA_STATUS_PENDING_AUDIT},
    CAPA_STATUS_CLOSED: set(),
}

# Master lookup lists for Critical / CAPA findings
AUDIT_FREQUENCIES = [
    'Daily', 'Weekly', 'Monthly', 'Quarterly', 'Half-Yearly', 'Yearly', 'N/A'
]

AUDIT_COMPONENTS = [
    'Activity', 'All other rooms in this floor', 'ASA Audit', 'Assembly',
    'Attendance Last page', 'Auxiliary', 'Book Review', 'Bulletin Board',
    'CCTV', 'Car Audit', 'Class Room Rounds', 'Deep cleaning', 'Dispersal',
    'Emergency Student Namelist', 'Fire Evacuvation list', 'Fire Evacuvation Map',
    'Front office', 'Gate Pass', 'Gps', 'Homework', 'Hostel Audit',
    'House Keeping', 'ID card defaults', 'Journal', 'KPI', 'Kural Recitation',
    'late Comers', 'Learning Walks', 'Lesson plan', 'MD Room',
    'Notebook / Workbook', 'Over all rounds', 'Parent Concern',
    'PE FIT -Staff Attendance', 'Prinicpal Office', 'PRM Prime Document',
    'Rifle', 'Sickbay', 'SOM Student', 'SOM Support team', 'Staff attendance',
    'Staff Late Reporting', 'Student Attendance register', 'Student Discipline',
    'Store Room', 'Teacher Observation', 'Transport Cleanliness',
    'Transport Complaint', 'Transport Entry /Exit', 'Transport Files',
    'Transport cleaniness', 'Transport paid and unpaid list', 'Vehiche Master record',
    'Walkie Talkie report', 'Washroom', 'N/A'
]

AUDIT_GRADES = [f'Grade {g}' for g in range(1, 13)] + ['N/A']

AUDIT_SECTIONS = ['A', 'B', 'C', 'A1', 'A2', 'AEP', 'N/A']

AUDIT_NATURE_OPTIONS = [
    'Critical', 'Manageable', 'All Well',
    'Non-compliance', 'Process deviation', 'Documentation gap',
    'Safety', 'Hygiene', 'Repeat observation'
]

AUDIT_SPECIFICATIONS = [
    'English', 'English CW', 'Maths', 'Science', 'Social',
    'L3 Hindi CW&CB', 'Journal', 'Assembly', 'Book review&video',
    'Tamil', 'Computer Science', 'N/A'
]

AUDIT_STAFF_NAMES = [
    'Aarthi A T', 'Aarthy Selvam', 'Abirami', 'Afrin', 'Akila', 'Akilandeswari',
    'Alagammal', 'Alangaram Joseph Dominic', 'Amsavalli', 'Anita', 'Anitha T',
    'Angalaeswari', 'Anushya', 'Aravind', 'Aravind - Guitar', 'Archana', 'Asha',
    'Asswah R', 'Ayyanar P', 'Bala - Western dance', 'Balamurugan Iyadurai Pillai',
    'Balamurugan Kayambu', 'Balasaravanan K', 'Beena Dr', 'Chandra - Silambam',
    'Chandrasekaran', 'Chandru PE', 'Chithra S', 'Christinal Shanthi E', 'Cuba Queen',
    'Deepika Kannan', 'Dhaniya', 'Divya', 'Durai Murugan Nagarajan', 'Edith',
    'Elavar Kuzhali', 'Fathima', 'Gayathri S', 'Gimbu', 'Gnanasundari', 'Gnanamani',
    'Govindammal', 'Gowsalya', 'Guruvammal', 'Gurusiddharth', 'Hari prasad - Drums',
    'Hariyaputhiran', 'Ilamathi Selvam Thevar', 'Indira', 'Infantia Vaz',
    'Jayashree - Classical dance', 'Jaison', 'Jana', 'Janane V M', 'Jayanthi',
    'Jegadheeshwari', 'Jerome', 'Jeyalakshmi', 'Jeyaseelan Paramasamy', 'Joe Daniel',
    'John Martin K', 'John Peter M', 'Jothirathinam', 'Jothyrathinam', 'Joy Jebha',
    'Joy Sheeba', 'Kalaiyarasi', 'Kalpana K', 'Kalyani', 'Kaniraja PE', 'Kanda samy',
    'Kannan B', 'Karpagam', 'Karthick Thiruppathiraj', 'Karthiga Ramachandran',
    'Karthika A', 'Karthikeyan', 'Kausik', 'Kaviya', 'Keerthana', 'Krishna Priya',
    'Kumaravel Mookaiah', 'Kuzhali', 'Lakshmanan', 'Mabu Batcha', 'Mallika',
    'Manoj PE', 'Mariyammal B', 'Meena', 'Meenakshi', 'Mohamed Aadhil S',
    'Mohamed Ali Jinna', 'Mohana Kannan', 'Murugan PE', 'Murugeshwari',
    'Murugeshwari G', 'Murugeshwari Pandyaraja', 'Muthiah', 'Muthukumar J', 'N/A',
    'Naveen', 'Naveena', 'Palaniyammal', 'Panju T', 'Panneer Chellam', 'Parasakthi',
    'Partha Sarathi', 'Parvathi', 'Paulin', 'Pear Morrish N', 'Pothumponnu',
    'Prabhakaran - Kung-fu', 'Pradeep S', 'Prakash - Taekwondo', 'Prakash - Yoga',
    'Radhakrishnan', 'Raja - Karate', 'Raja - Keyboard', 'Ramkumari',
    'Ramesh Kumar Ramachandran', 'Ramesh P', 'Regis Sidharth', 'Rhagavan moorthy',
    'Sakthivel S/O Tharmaraj', 'Salmy', 'Santhi S', 'Sangeetha Dr', 'Sathish Kumar K',
    'Sathyapriya', 'Selvam Pushari Nalla Perumal Thevar', 'Shalini Joseph',
    'Shalini Nagendra Babu', 'Shanmugavalli', 'Sharmili', 'Shayana Fransis',
    'Shrinithee', 'Silambarasi', 'Sivaranjani R', 'Sonia', 'Sudha', 'Sundari Jeyaram',
    'Surya PE', 'Suryakala', 'Susirekha', 'Sutha R', 'Swarnamathi', 'Thanga Kanaga',
    'Thirivengadam', 'Thirubhuvan', 'Thulasi', 'Uma Maheshwaran PE', 'Uma Maheswari',
    'Uma Rani', 'Umarani B', 'Urban', 'Vaiyapuri G', 'Vairamani B', 'Vanitha',
    'Varatharajan PE', 'Vengadeswari Arumugam', 'Vijaya Chellapandi', 'Vijay N',
    'Vijayalakshmi', 'Viji', 'Vigneshwari K', 'Vimalraj', 'Vinaya PE',
    'Vinith Sharan S', 'Vinothini', 'Viswanath', 'Vivek', 'Zenofer'
]

def get_audit_lookups():
    """Canonical lookup collections for Critical / CAPA finding form."""
    auditors = []
    try:
        user_auditors = [u.username for u in User.query.filter(
            or_(User.team_id == AUDIT_TEAM_ID, User.role.in_(AUDIT_ROLES))
        ).order_by(User.username).all()]
        auditors.extend(user_auditors)
    except Exception:
        pass
    for default_auditor in ['Christinal', 'Ilamathi', 'Jaison', 'Fyrose', 'Sangamitra', 'auditteam', 'admin']:
        if default_auditor not in auditors:
            auditors.append(default_auditor)

    return {
        'frequencies': AUDIT_FREQUENCIES,
        'components': AUDIT_COMPONENTS,
        'auditors': sorted(list(set(auditors))),
        'staff_names': AUDIT_STAFF_NAMES,
        'grades': AUDIT_GRADES,
        'sections': AUDIT_SECTIONS,
        'specifications': AUDIT_SPECIFICATIONS,
        'nature_options': AUDIT_NATURE_OPTIONS,
        'priorities': CAPA_PRIORITIES,
    }

# =====================================================
#  Permissions
# =====================================================

def can_audit(user):
    """True for users allowed to raise findings and perform audit review."""
    if user is None or not getattr(user, 'is_authenticated', False):
        return False
    return user.team_id == AUDIT_TEAM_ID or user.role in AUDIT_ROLES


def can_view_finding(finding, user):
    """Authorization check for viewing a finding and its history.

    - Auditors / MD / Admin see all findings.
    - Team Leads see findings assigned to or affecting members of their own team,
      or findings directly assigned to or raised by the Team Lead.
    - Team Members see only findings assigned to them (or affecting them).
    """
    if not getattr(user, 'is_authenticated', False):
        return False
    if can_audit(user):
        return True
    if finding.recipient_id == user.user_id or finding.submitted_by == user.user_id:
        return True
    if user.role == 'Team Lead' and user.team_id:
        if finding.recipient and finding.recipient.team_id == user.team_id:
            return True
        if finding.staff_name:
            staff_user = User.query.filter(
                func.lower(User.username) == func.lower(finding.staff_name)
            ).first()
            if staff_user and staff_user.team_id == user.team_id:
                return True
        return False
    if finding.staff_name and user.username and finding.staff_name.lower() == user.username.lower():
        return True
    return False


def audit_required(view):
    """Restrict a view to users satisfying can_audit()."""
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not can_audit(current_user):
            if request.accept_mimetypes.best == 'application/json' or request.is_json:
                return jsonify({'error': 'Not authorized.'}), 403
            flash('You are not authorized to access the Critical audit workflow.', 'danger')
            return redirect(url_for('critical.critical_home'))
        return view(*args, **kwargs)
    return wrapper


# =====================================================
#  Helpers
# =====================================================

def team_display(user):
    """Human-readable team name for a user ('Audit', 'Academic', ...)."""
    if user is None:
        return 'Unassigned'
    team_name = user.team.team_name if user.team else None
    if not team_name:
        return 'Unassigned'
    return TEAM_DISPLAY_NAMES.get(team_name, team_name)


def user_label(user):
    """`username - Team - Role`, the recipient display available from `users`.

    The users table carries no full name or employee id, so username is the
    identifier shown. See the schema notes in the project report.
    """
    if user is None:
        return 'Unknown user'
    return f'{user.username} - {team_display(user)} - {user.role}'

def next_audit_reference(for_date=None):
    """Build the next AUD-YYYY-NNNN reference for the given year.

    audit_reference carries a UNIQUE constraint and the create view retries on
    IntegrityError, so a race between two auditors cannot produce a duplicate.
    """
    year = (for_date or now_ist().date()).year
    prefix = f'AUD-{year}-'
    last = (db.session.query(CapaFinding.audit_reference)
            .filter(CapaFinding.audit_reference.like(prefix + '%'))
            .order_by(CapaFinding.audit_reference.desc())
            .first())
    seq = 1
    if last and last[0]:
        try:
            seq = int(str(last[0]).rsplit('-', 1)[-1]) + 1
        except (ValueError, IndexError):
            seq = 1
    return f'{prefix}{seq:04d}'


def log_event(finding, user, action, old_status=None, new_status=None, comment=None):
    """Append one immutable row to the CAPA audit trail."""
    event = CapaEvent(
        finding_id=finding.form_id,
        user_id=user.user_id,
        action=action,
        old_status=old_status,
        new_status=new_status,
        comment=comment,
    )
    db.session.add(event)
    return event


def transition(finding, new_status, user, action, comment=None):
    """Move a finding to new_status, refusing illegal transitions.

    The only place CapaFinding.status is assigned. Raises ValueError when the
    requested transition is not in ALLOWED_TRANSITIONS.
    """
    old_status = finding.status
    if new_status not in ALLOWED_TRANSITIONS.get(old_status, set()):
        raise ValueError(
            f'Illegal CAPA transition {old_status} -> {new_status} '
            f'for {finding.audit_reference}.'
        )
    finding.status = new_status
    log_event(finding, user, action, old_status, new_status, comment)
    return finding

def store_uploads(files, finding, stage, user):
    """Persist uploads into the existing FileStorage table and link them.

    Reuses FileStorage (the app's single file system) and records one
    CapaAttachment row per file, so any stage can carry multiple files.
    Raises ValueError when a file exceeds MAX_UPLOAD_BYTES.
    """
    stored = []
    for upload in files or []:
        if not upload or not upload.filename:
            continue

        upload.seek(0, 2)
        file_size = upload.tell()
        upload.seek(0)
        if file_size > MAX_UPLOAD_BYTES:
            raise ValueError(f'File {upload.filename} is too large. Maximum size is 200MB.')
        if file_size == 0:
            continue

        original_filename = secure_filename(upload.filename)
        timestamp = now_ist().strftime('%Y%m%d_%H%M%S')
        file_record = FileStorage(
            filename=f'{timestamp}_{original_filename}',
            original_filename=original_filename,
            file_data=upload.read(),
            file_size=file_size,
            mime_type=upload.content_type or 'application/octet-stream',
            uploaded_by=user.user_id,
        )
        db.session.add(file_record)
        db.session.flush()

        db.session.add(CapaAttachment(
            finding_id=finding.form_id,
            file_id=file_record.file_id,
            stage=stage,
            uploaded_by=user.user_id,
        ))
        stored.append(file_record)
    return stored


def bust_user_cache(user_id):
    """Drop the per-user cached pages that embed the nav badge.

    dashboard() and my_history() are cached for 300s with per_user_cache_key,
    which freezes the rendered navigation. Clearing the affected user's entries
    keeps the Critical badge honest after a workflow transition.
    """
    for path in ('/dashboard', '/my_history'):
        try:
            cache.delete(f'user:{user_id}|path:{path}|qs:')
        except Exception:
            pass

def bust_team_lead_cache(team_id):
    """Drop the per-user cached pages for the Team Lead(s) of team_id."""
    if not team_id:
        return
    lead_ids = [r[0] for r in db.session.query(User.user_id).filter(
        User.team_id == team_id,
        User.role == 'Team Lead'
    ).all()]
    for lid in lead_ids:
        bust_user_cache(lid)

def pending_critical_count(user):
    """Items needing this user's attention -- drives the nav badge.

    - Recipient: counts findings awaiting their response or revision.
    - Team Lead: counts findings awaiting their team's response or revision.
    - Auditor: counts findings sitting in audit review.
    """
    if not getattr(user, 'is_authenticated', False):
        return 0

    if user.is_team_lead and user.team_id:
        team_user_ids = [r[0] for r in db.session.query(User.user_id).filter_by(team_id=user.team_id).all()]
        team_usernames = [r[0] for r in db.session.query(User.username).filter_by(team_id=user.team_id).all()]
        clauses = [db.and_(
            or_(
                CapaFinding.recipient_id == user.user_id,
                CapaFinding.recipient_id.in_(team_user_ids),
                CapaFinding.staff_name.in_(team_usernames),
            ),
            CapaFinding.status.in_((CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED)),
        )]
        if can_audit(user):
            clauses.append(CapaFinding.status == CAPA_STATUS_PENDING_AUDIT)
    elif can_audit(user):
        clauses = [
            CapaFinding.status == CAPA_STATUS_PENDING_AUDIT,
            db.and_(
                CapaFinding.recipient_id == user.user_id,
                CapaFinding.status.in_((CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED)),
            )
        ]
    else:
        clauses = [db.and_(
            or_(
                CapaFinding.recipient_id == user.user_id,
                CapaFinding.staff_name == user.username,
            ),
            CapaFinding.status.in_((CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED)),
        )]

    try:
        return CapaFinding.query.filter(or_(*clauses)).count()
    except Exception:
        return 0


def visible_findings_query(user):
    """Base query scoped to what `user` is allowed to see.

    Strict server-side authorization:
    - MD / Admin / Audit: organization-wide visibility across all teams.
    - Team Lead: findings where the recipient or affected staff member belongs to
      the logged-in user's team, or where the Team Lead is the recipient or creator.
      Other teams' findings are excluded at the SQL level.
    - Team Member: only findings assigned to or affecting the member.
    """
    if not getattr(user, 'is_authenticated', False):
        return CapaFinding.query.filter(db.text('1=0'))

    if can_audit(user):
        return CapaFinding.query

    if user.role == 'Team Lead' and user.team_id:
        team_member_ids = [r[0] for r in db.session.query(User.user_id).filter(User.team_id == user.team_id).all()]
        team_usernames = [r[0] for r in db.session.query(User.username).filter(User.team_id == user.team_id).all()]

        return CapaFinding.query.filter(
            or_(
                CapaFinding.recipient_id == user.user_id,
                CapaFinding.recipient_id.in_(team_member_ids),
                CapaFinding.staff_name.in_(team_usernames),
                CapaFinding.submitted_by == user.user_id,
            )
        )

    return CapaFinding.query.filter(
        or_(
            CapaFinding.recipient_id == user.user_id,
            CapaFinding.staff_name == user.username,
            CapaFinding.submitted_by == user.user_id,
        )
    )


def _clean(value, limit=None):
    """Trim a submitted field; returns '' for missing values."""
    text = (value or '').strip()
    if limit:
        text = text[:limit]
    return text

# =====================================================
#  Routes
# =====================================================

@critical_bp.route('/critical', methods=['GET'])
@login_required
def critical_home():
    """Role-aware inbox: audit users see every finding, recipients see theirs."""
    status_filter = request.args.get('status') or ''
    query = visible_findings_query(current_user)

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
    """Creation form -- audit finding fields only."""
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
    """Create an audit finding and assign it to one recipient."""
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
        # Lets the picker keep showing the chosen user if validation sends the form back.
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
        return reject('You cannot assign a finding to yourself -- an auditor '
                      'may not review their own CAPA.')

    audit_date = now_ist().date()
    if audit_date_raw:
        try:
            audit_date = datetime.strptime(audit_date_raw, '%Y-%m-%d').date()
        except ValueError:
            return reject('Audit Date must be a valid date (YYYY-MM-DD).')

    uploads = request.files.getlist('attachments')

    # The `auditteam` account has team_id = NULL, so fall back to the audit team.
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
            # Another auditor took this reference; retry with the next one.
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
    flash(f'Finding {finding.audit_reference} created. New CAPA assigned to '
          f'{recipient.username}.', 'success')
    return redirect(url_for('critical.finding_detail', finding_id=finding.form_id))


@critical_bp.route('/critical/<int:finding_id>/edit', methods=['GET'])
@login_required
@audit_required
def edit_finding(finding_id):
    """Edit finding parameters -- available to auditors when finding is not closed."""
    finding = CapaFinding.query.get_or_404(finding_id)
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
    """Update finding details."""
    finding = CapaFinding.query.get_or_404(finding_id)
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
    """One finding: read-only history plus whichever panel the viewer may use."""
    finding = CapaFinding.query.get_or_404(finding_id)
    if not can_view_finding(finding, current_user):
        flash('You are not authorized to view this CAPA finding.', 'danger')
        return redirect(url_for('critical.critical_home'))

    is_auditor = can_audit(current_user)
    is_recipient = finding.recipient_id == current_user.user_id

    # A recipient may respond while the ball is in their court; an auditor may
    # review only when the CAPA is not their own.
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
    """Recipient picker source -- the real users table, all teams."""
    # A JSON endpoint answers with JSON: audit_required would redirect here,
    # because fetch() sends Accept: */* rather than application/json.
    if not can_audit(current_user):
        return jsonify({'error': 'Not authorized.'}), 403

    term = _clean(request.args.get('q'))
    query = User.query
    if term:
        like = f'%{term}%'
        query = (query.outerjoin(Team, User.team_id == Team.team_id)
                 .filter(or_(User.username.ilike(like),
                             User.role.ilike(like),
                             Team.team_name.ilike(like))))
    users = query.order_by(User.username).limit(50).all()
    return jsonify({'users': [{
        'user_id': u.user_id,
        'username': u.username,
        'team': team_display(u),
        'role': u.role,
        'label': user_label(u),
    } for u in users if u.user_id != current_user.user_id]})

def bust_audit_caches():
    """Refresh cached pages for every user who can act on audit review."""
    try:
        auditors = User.query.filter(
            or_(User.team_id == AUDIT_TEAM_ID, User.role.in_(AUDIT_ROLES))
        ).all()
    except Exception:
        return
    for auditor in auditors:
        bust_user_cache(auditor.user_id)


@critical_bp.route('/critical/<int:finding_id>/respond', methods=['POST'])
@login_required
def submit_response(finding_id):
    """Recipient submits (or revises) Action Taken Report, RCA and CAPA 1."""
    finding = CapaFinding.query.get_or_404(finding_id)
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
    """Audit enters CAPA 2 and accepts (closing) or rejects with justification."""
    finding = CapaFinding.query.get_or_404(finding_id)
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
            message = (f'CAPA revision required -- {finding.audit_reference} returned '
                       f'to {finding.recipient.username}.')
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
