from datetime import datetime
from app import db


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('programmes.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    year_of_study = db.Column(db.Integer, default=1)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))
    address = db.Column(db.Text)
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    qr_code_path = db.Column(db.String(255))
    status = db.Column(db.String(20), default='active')

    programme = db.relationship('Programme', backref='students')
    department = db.relationship('Department', backref='students')
    results = db.relationship('Result', backref='student', lazy='dynamic')
    clinical_postings = db.relationship('ClinicalPosting', backref='student', lazy='dynamic')
    submissions = db.relationship('AssignmentSubmission', backref='student', lazy='dynamic')

    def __repr__(self):
        return f'<Student {self.student_id}>'
