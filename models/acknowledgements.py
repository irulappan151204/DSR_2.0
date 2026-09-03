from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo
from timezone_utils import now_ist

class Acknowledgement(db.Model):
    __tablename__ = 'acknowledgements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    acknowledged_at = db.Column(db.DateTime(timezone=True), nullable=True, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))

    user = db.relationship('User', backref='acknowledgements')

    def __repr__(self):
        return f'<Acknowledgement {self.user_id} {self.date} {self.acknowledged_at}>'

