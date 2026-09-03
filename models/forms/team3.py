from extensions import db
from .base import BaseForm

class Team3Audit(BaseForm):
    __tablename__ = 'team3_audit'

    frequency = db.Column(db.String(50), nullable=False)
    audit_components = db.Column(db.Text, nullable=False)
    audit_by = db.Column(db.String(100), nullable=False)
    audit_time = db.Column(db.Time, nullable=False)
    issue_nature = db.Column(db.String(20), nullable=False)  # critical/manageable/all_well
    audit_remarks = db.Column(db.Text, nullable=True)
    # Relationships
    submitter = db.relationship('User', foreign_keys='Team3Audit.submitted_by', backref=db.backref('submitted_team3_audit', lazy=True)) 


class Team3NewAudit(BaseForm):
    __tablename__ = 'team3_new_audit'

    frequency = db.Column(db.String(50), nullable=False)
    component = db.Column(db.Text, nullable=False)
    audited_by = db.Column(db.String(100), nullable=False)
    staff_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    specification = db.Column(db.Text, nullable=True)
    issue_nature = db.Column(db.String(20), nullable=False)  # critical/manageable/all_well
    remark = db.Column(db.Text, nullable=True)

    # Optional: store uploaded media file in DB BLOB store
    media_file_id = db.Column(db.Integer, db.ForeignKey('file_storage.file_id'), nullable=True)

    # Relationships
    submitter = db.relationship(
        'User',
        foreign_keys='Team3NewAudit.submitted_by',
        backref=db.backref('submitted_team3_new_audit', lazy=True)
    )
    media_file = db.relationship('FileStorage', foreign_keys=[media_file_id], backref='team3_new_audits')


