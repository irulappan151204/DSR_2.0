from datetime import datetime
from functools import wraps
from flask import request, redirect, url_for, flash, jsonify
from flask_login import current_user
from sqlalchemy import or_, func
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
from repositories.capa_repository import can_audit, AUDIT_TEAM_ID, AUDIT_ROLES

MAX_UPLOAD_BYTES = 200 * 1024 * 1024
TEAM_DISPLAY_NAMES = {'Team 1': 'Academic', 'Team 2': 'Admin', 'Team 3': 'Audit'}

ALLOWED_TRANSITIONS = {
    CAPA_STATUS_OPEN: {CAPA_STATUS_PENDING_RECIPIENT},
    CAPA_STATUS_PENDING_RECIPIENT: {CAPA_STATUS_PENDING_AUDIT},
    CAPA_STATUS_PENDING_AUDIT: {CAPA_STATUS_CLOSED, CAPA_STATUS_REVISION_REQUIRED},
    CAPA_STATUS_REVISION_REQUIRED: {CAPA_STATUS_PENDING_AUDIT},
    CAPA_STATUS_CLOSED: set(),
}

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

def can_view_finding(finding, user):
    """Authorization check for viewing a finding and its history."""
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

def team_display(user):
    """Human-readable team name for a user ('Audit', 'Academic', ...)."""
    if user is None:
        return 'Unassigned'
    team_name = user.team.team_name if user.team else None
    if not team_name:
        return 'Unassigned'
    return TEAM_DISPLAY_NAMES.get(team_name, team_name)

def user_label(user):
    """username - Team - Role display label."""
    if user is None:
        return 'Unknown user'
    return f'{user.username} - {team_display(user)} - {user.role}'

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
    """Move a finding to new_status, refusing illegal transitions."""
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
    """Persist uploads into FileStorage and link them."""
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
    """Drop the per-user cached pages that embed the nav badge."""
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

def _clean(value, limit=None):
    """Trim a submitted field; returns '' for missing values."""
    text = (value or '').strip()
    if limit:
        text = text[:limit]
    return text

def get_pending_critical_context(current_user):
    """Inject the Critical/CAPA pending count into template context."""
    from repositories.capa_repository import get_pending_critical_count
    if not getattr(current_user, 'is_authenticated', False):
        return {
            'has_pending_critical': False,
            'pending_critical_count': 0,
            'can_view_critical': False
        }

    pending = get_pending_critical_count(current_user)
    return {
        'has_pending_critical': pending > 0,
        'pending_critical_count': pending,
        'can_view_critical': True
    }

