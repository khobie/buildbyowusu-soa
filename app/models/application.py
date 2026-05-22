from datetime import datetime
from app import db


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    tracking_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('programmes.id'), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    nationality = db.Column(db.String(50))
    address = db.Column(db.Text)
    education_background = db.Column(db.Text)
    work_experience = db.Column(db.Text)
    document_path = db.Column(db.String(255))
    transcript_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')
    admin_notes = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Application {self.tracking_id}>'
