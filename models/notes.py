from extensions import db
from datetime import datetime
from timezone_utils import now_ist

class Note(db.Model):
    __tablename__ = 'user_notes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=True)
    content = db.Column(db.Text, nullable=False)
    color = db.Column(db.String(30), nullable=False, default='default')
    priority = db.Column(db.String(20), nullable=False, default='medium')
    is_pinned = db.Column(db.Boolean, nullable=False, default=False)
    is_done = db.Column(db.Boolean, nullable=False, default=False, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    is_archived = db.Column(db.Boolean, nullable=False, default=False)
    reminder_at = db.Column(db.DateTime, nullable=True)
    reminder_seen = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: now_ist().replace(tzinfo=None))
    updated_at = db.Column(db.DateTime, nullable=False, default=lambda: now_ist().replace(tzinfo=None), onupdate=lambda: now_ist().replace(tzinfo=None))

    user = db.relationship('User', backref=db.backref('notes', cascade='all, delete-orphan', lazy='dynamic'))

    def to_dict(self):
        curr_time = now_ist().replace(tzinfo=None)
        is_due = bool(not self.is_done and self.reminder_at and self.reminder_at <= curr_time and not self.reminder_seen)
        
        # Calculate human-friendly reminder status
        reminder_status = None
        reminder_relative = None
        if self.is_done:
            reminder_status = 'completed'
        elif self.reminder_at:
            diff_seconds = (self.reminder_at - curr_time).total_seconds()
            if not self.reminder_seen and self.reminder_at <= curr_time:
                reminder_status = 'due'
                mins_overdue = int(abs(diff_seconds) / 60)
                if mins_overdue < 1:
                    reminder_relative = 'Due just now'
                elif mins_overdue < 60:
                    reminder_relative = f'Overdue by {mins_overdue}m'
                elif mins_overdue < 1440:
                    reminder_relative = f'Overdue by {mins_overdue // 60}h'
                else:
                    reminder_relative = f'Overdue by {mins_overdue // 1440}d'
            elif self.reminder_at > curr_time:
                reminder_status = 'upcoming'
                mins_left = int(diff_seconds / 60)
                if mins_left < 60:
                    reminder_relative = f'In {mins_left}m'
                elif mins_left < 1440:
                    reminder_relative = f'In {mins_left // 60}h'
                else:
                    reminder_relative = f'In {mins_left // 1440}d'
            else:
                reminder_status = 'dismissed'

        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title or '',
            'content': self.content or '',
            'color': self.color or 'default',
            'priority': self.priority or 'medium',
            'is_pinned': bool(self.is_pinned),
            'is_done': bool(self.is_done),
            'completed_at': self.completed_at.strftime('%d %b %Y, %I:%M %p') if self.completed_at else None,
            'is_archived': bool(self.is_archived),
            'reminder_at': self.reminder_at.strftime('%Y-%m-%dT%H:%M') if self.reminder_at else None,
            'reminder_at_display': self.reminder_at.strftime('%d %b %Y, %I:%M %p') if self.reminder_at else None,
            'reminder_status': reminder_status,
            'reminder_relative': reminder_relative,
            'reminder_seen': bool(self.reminder_seen),
            'is_reminder_due': is_due,
            'created_at': self.created_at.strftime('%d %b %Y, %I:%M %p') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%d %b %Y, %I:%M %p') if self.updated_at else None,
        }

    def __repr__(self):
        return f'<Note {self.id} user={self.user_id} title={self.title!r} done={self.is_done}>'
