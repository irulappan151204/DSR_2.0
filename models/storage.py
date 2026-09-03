from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo
from timezone_utils import now_ist

class FileStorage(db.Model):
    __tablename__ = 'file_storage'
    
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_data = db.Column(db.LargeBinary(length=4294967295), nullable=False)  # LONGBLOB storage (up to 4GB)
    file_size = db.Column(db.Integer, nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    uploaded_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(ZoneInfo('Asia/Kolkata')))
    
    # Relationships
    user = db.relationship('User', backref='uploaded_files')
    
    def __repr__(self):
        return f'<FileStorage {self.original_filename}>'

