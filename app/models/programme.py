from datetime import datetime
from app import db


class Programme(db.Model):
    __tablename__ = 'programmes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    level = db.Column(db.String(50))
    duration = db.Column(db.String(50))
    description = db.Column(db.Text)
    entry_requirements = db.Column(db.Text)
    tuition_fee = db.Column(db.String(100))
    curriculum = db.Column(db.Text)
    clinical_structure = db.Column(db.Text)
    is_featured = db.Column(db.Boolean, default=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    courses = db.relationship('Course', backref='programme', lazy='dynamic', cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='programme', lazy='dynamic')

    def __repr__(self):
        return f'<Programme {self.code}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    programme_id = db.Column(db.Integer, db.ForeignKey('programmes.id'), nullable=False)
    code = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    credits = db.Column(db.Integer, default=3)
    semester = db.Column(db.Integer)
    year = db.Column(db.Integer)
    description = db.Column(db.Text)

    materials = db.relationship('CourseMaterial', backref='course', lazy='dynamic')
    results = db.relationship('Result', backref='course', lazy='dynamic')
    assignments = db.relationship('Assignment', backref='course', lazy='dynamic')
    timetables = db.relationship('Timetable', backref='course', lazy='dynamic')

    def __repr__(self):
        return f'<Course {self.code}>'
