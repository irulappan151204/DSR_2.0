from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo
from timezone_utils import now_ist
from .forms.base import BaseForm


# =====================================================
#  CAPA / Critical audit workflow
#  Audit -> Recipient -> Audit Review -> Closure
# =====================================================

# Workflow statuses. The backend is the only writer of CapaFinding.status --
# these values are never rendered as a user-editable form field.
CAPA_STATUS_OPEN = 'OPEN'
CAPA_STATUS_PENDING_RECIPIENT = 'PENDING_RECIPIENT_RESPONSE'
CAPA_STATUS_PENDING_AUDIT = 'PENDING_AUDIT_REVIEW'
CAPA_STATUS_REVISION_REQUIRED = 'CAPA_REVISION_REQUIRED'
CAPA_STATUS_CLOSED = 'CLOSED'

CAPA_STATUSES = (
    CAPA_STATUS_OPEN,
    CAPA_STATUS_PENDING_RECIPIENT,
    CAPA_STATUS_PENDING_AUDIT,
    CAPA_STATUS_REVISION_REQUIRED,
    CAPA_STATUS_CLOSED,
)

CAPA_STATUS_LABELS = {
    CAPA_STATUS_OPEN: 'Open',
    CAPA_STATUS_PENDING_RECIPIENT: 'Pending Recipient Response',
    CAPA_STATUS_PENDING_AUDIT: 'Pending Audit Review',
    CAPA_STATUS_REVISION_REQUIRED: 'CAPA Revision Required',
    CAPA_STATUS_CLOSED: 'Closed',
}

# CSS suffix for the existing .status-badge convention used across the app.
CAPA_STATUS_CSS = {
    CAPA_STATUS_OPEN: 'capa-open',
    CAPA_STATUS_PENDING_RECIPIENT: 'capa-pending-recipient',
    CAPA_STATUS_PENDING_AUDIT: 'capa-pending-audit',
    CAPA_STATUS_REVISION_REQUIRED: 'capa-revision',
    CAPA_STATUS_CLOSED: 'capa-closed',
}

CAPA_PRIORITIES = ('Low', 'Medium', 'High', 'Critical')

CAPA_DECISION_ACCEPTED = 'ACCEPTED'
CAPA_DECISION_NOT_ACCEPTED = 'NOT_ACCEPTED'

# Attachment stages -- which step of the workflow uploaded the evidence.
CAPA_STAGE_FINDING = 'FINDING'
CAPA_STAGE_RESPONSE = 'RESPONSE'
CAPA_STAGE_REVIEW = 'REVIEW'

class CapaFinding(BaseForm):
    """One audit finding carried through the full CAPA workflow.

    Inherits form_id / team_id / submitted_by / submitted_at from BaseForm, so
    the creator and creation time live in submitted_by / submitted_at (exposed
    below as created_by / created_at for readability).
    """
    __tablename__ = 'capa_findings'

    # --- Audit finding (created by Team 3 / Audit, immutable afterwards) ---
    audit_reference = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    frequency = db.Column(db.String(50), nullable=True)
    component = db.Column(db.String(255), nullable=True)
    audited_by = db.Column(db.String(100), nullable=True)
    staff_name = db.Column(db.String(100), nullable=True)
    grade = db.Column(db.String(50), nullable=True)
    section = db.Column(db.String(50), nullable=True)
    specification = db.Column(db.Text, nullable=True)
    nature_of_issue = db.Column(db.String(100), nullable=False)
    remark = db.Column(db.Text, nullable=True)
    priority = db.Column(db.String(20), nullable=False, default='Medium')
    audit_date = db.Column(db.Date, nullable=False)

    # Recipient is stored as a reference to the real users table, never as text.
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    # --- Workflow state (backend-controlled only) ---
    status = db.Column(db.String(32), nullable=False, default=CAPA_STATUS_PENDING_RECIPIENT)
    revision_count = db.Column(db.Integer, nullable=False, default=0)

    # --- Recipient response (CAPA 1) ---
    action_taken_report = db.Column(db.Text, nullable=True)
    root_cause_analysis = db.Column(db.Text, nullable=True)
    capa_1 = db.Column(db.Text, nullable=True)
    capa_1_submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    capa_1_submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # --- Audit response (CAPA 2) ---
    capa_2 = db.Column(db.Text, nullable=True)
    capa_2_submitted_at = db.Column(db.DateTime(timezone=True), nullable=True)
    capa_2_submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    # --- Audit decision / closure ---
    audit_decision = db.Column(db.String(16), nullable=True)  # ACCEPTED | NOT_ACCEPTED
    audit_justification = db.Column(db.Text, nullable=True)   # mandatory when NOT_ACCEPTED
    audit_reviewed_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
    audit_reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    closed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    updated_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')),
                           onupdate=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    # --- Relationships (explicit foreign_keys: several columns point at users) ---
    creator = db.relationship('User', foreign_keys='CapaFinding.submitted_by',
                              backref=db.backref('created_capa_findings', lazy='dynamic'))
    recipient = db.relationship('User', foreign_keys='CapaFinding.recipient_id',
                                backref=db.backref('assigned_capa_findings', lazy='dynamic'))
    capa_1_author = db.relationship('User', foreign_keys='CapaFinding.capa_1_submitted_by')
    capa_2_author = db.relationship('User', foreign_keys='CapaFinding.capa_2_submitted_by')
    reviewer = db.relationship('User', foreign_keys='CapaFinding.audit_reviewed_by')

    # id is the tie-breaker: MySQL DATETIME has no sub-second precision, so
    # several events written in the same request share one created_at.
    events = db.relationship('CapaEvent', back_populates='finding',
                             order_by='CapaEvent.created_at, CapaEvent.id',
                             cascade='all, delete-orphan', lazy='select')
    attachments = db.relationship('CapaAttachment', back_populates='finding',
                                  order_by='CapaAttachment.uploaded_at, CapaAttachment.id',
                                  cascade='all, delete-orphan', lazy='select')

    # created_by / created_at are the spec's names for BaseForm's columns.
    @property
    def created_by(self):
        return self.submitted_by

    @property
    def created_at(self):
        return self.submitted_at

    @property
    def status_label(self):
        return CAPA_STATUS_LABELS.get(self.status, self.status)

    @property
    def status_css(self):
        return CAPA_STATUS_CSS.get(self.status, 'capa-open')

    @property
    def is_closed(self):
        return self.status == CAPA_STATUS_CLOSED

    @property
    def awaiting_recipient(self):
        return self.status in (CAPA_STATUS_PENDING_RECIPIENT, CAPA_STATUS_REVISION_REQUIRED)

    @property
    def awaiting_audit_review(self):
        return self.status == CAPA_STATUS_PENDING_AUDIT

    def files_for_stage(self, stage):
        return [a for a in self.attachments if a.stage == stage]

    def __repr__(self):
        return f'<CapaFinding {self.audit_reference} {self.status}>'

class CapaEvent(db.Model):
    """Append-only audit trail for a CAPA finding.

    Rows are never updated or deleted -- every workflow action adds one row so
    the full history (who, what, when, old status -> new status) is preserved.
    """
    __tablename__ = 'capa_events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finding_id = db.Column(db.Integer, db.ForeignKey('capa_findings.form_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    action = db.Column(db.String(64), nullable=False)
    old_status = db.Column(db.String(32), nullable=True)
    new_status = db.Column(db.String(32), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False,
                           default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    finding = db.relationship('CapaFinding', back_populates='events')
    user = db.relationship('User', foreign_keys=[user_id])

    def __repr__(self):
        return f'<CapaEvent {self.finding_id} {self.action}>'


class CapaAttachment(db.Model):
    """Links a CAPA finding to files in the existing FileStorage table.

    A join table rather than FK columns on capa_findings, so each workflow stage
    can carry any number of files without duplicating the file-storage system.
    """
    __tablename__ = 'capa_attachments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    finding_id = db.Column(db.Integer, db.ForeignKey('capa_findings.form_id'), nullable=False, index=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file_storage.file_id'), nullable=False)
    stage = db.Column(db.String(16), nullable=False, default=CAPA_STAGE_FINDING)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False,
                            default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    finding = db.relationship('CapaFinding', back_populates='attachments')
    file = db.relationship('FileStorage', foreign_keys=[file_id])
    uploader = db.relationship('User', foreign_keys=[uploaded_by])

    def __repr__(self):
        return f'<CapaAttachment {self.finding_id} {self.stage} {self.file_id}>'