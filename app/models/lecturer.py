from datetime import datetime
from app import db


class Lecturer(db.Model):
    __tablename__ = 'lecturers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    staff_id = db.Column(db.String(20), unique=True, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    title = db.Column(db.String(50))
    specialization = db.Column(db.String(100))
    qualification = db.Column(db.String(200))
    office_location = db.Column(db.String(100))
    hire_date = db.Column(db.Date, default=datetime.utcnow)

    department = db.relationship('Department', backref='lecturers')
    supervised_postings = db.relationship('ClinicalPosting', backref='supervisor', lazy='dynamic')

    def __repr__(self):
        return f'<Lecturer {self.staff_id}>'
