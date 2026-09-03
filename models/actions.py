from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo
from timezone_utils import now_ist

class Action(db.Model):
    __tablename__ = 'actions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    assigned_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    action_text = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    status = db.Column(db.String(20), nullable=False, default='Pending')
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    completion_message = db.Column(db.Text, nullable=True)
    loop_message = db.Column(db.Text, nullable=True)
    parent_action_id = db.Column(db.Integer, db.ForeignKey('actions.id'), nullable=True)

    # Relationships
    assigned_user = db.relationship('User', foreign_keys=[assigned_user_id], backref='assigned_actions')
    creator = db.relationship('User', foreign_keys=[created_by], backref='created_actions')
    parent_action = db.relationship('Action', remote_side=[id], backref='child_actions')

    @property
    def time_taken(self):
        if self.completed_at:
            return self.completed_at - self.created_at
        return None

