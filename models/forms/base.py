from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

class BaseForm(db.Model):
    __abstract__ = True
    
    form_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    submitted_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(ZoneInfo("Asia/Kolkata"))
    )

# Team 1 Form Model    
