from sqlalchemy import or_, func
from extensions import db
from models import (
    CapaFinding, User, Team,
    CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED, CAPA_STATUS_PENDING_AUDIT
)
from timezone_utils import now_ist

AUDIT_TEAM_ID = 3
AUDIT_ROLES = ('MD', 'Admin')

def can_audit(user):
    """True for users allowed to raise findings and perform audit review."""
    if user is None or not getattr(user, 'is_authenticated', False):
        return False
    return user.team_id == AUDIT_TEAM_ID or user.role in AUDIT_ROLES

def get_finding_by_id(finding_id):
    """Retrieve a finding by ID."""
    return CapaFinding.query.get(finding_id)

def get_finding_or_404(finding_id):
    """Retrieve a finding by ID or raise 404."""
    return CapaFinding.query.get_or_404(finding_id)

def next_audit_reference(for_date=None):
    """Build the next AUD-YYYY-NNNN reference for the given year."""
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

def get_visible_findings_query(user):
    """Base query scoped to what user is allowed to see."""
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

def get_pending_critical_count(user):
    """Items needing this user's attention -- drives the nav badge."""
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

def search_users_query(term, current_user_id):
    """Recipient picker query."""
    query = User.query
    if term:
        like = f'%{term}%'
        query = (query.outerjoin(Team, User.team_id == Team.team_id)
                 .filter(or_(User.username.ilike(like),
                             User.role.ilike(like),
                             Team.team_name.ilike(like))))
    return query.order_by(User.username).limit(50).all()
