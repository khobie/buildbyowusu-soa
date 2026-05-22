from datetime import datetime
from app import db


class ClinicalPosting(db.Model):
    __tablename__ = 'clinical_postings'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    hospital_name = db.Column(db.String(150), nullable=False)
    department_unit = db.Column(db.String(100))
    posting_type = db.Column(db.String(50))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('lecturers.id'))
    status = db.Column(db.String(20), default='scheduled')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    attendances = db.relationship('Attendance', backref='posting', lazy='dynamic', cascade='all, delete-orphan')


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    posting_id = db.Column(db.Integer, db.ForeignKey('clinical_postings.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    present = db.Column(db.Boolean, default=True)
    hours = db.Column(db.Float, default=8.0)
    remarks = db.Column(db.String(200))

    __table_args__ = (db.UniqueConstraint('posting_id', 'date'),)
