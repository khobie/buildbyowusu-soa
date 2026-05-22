from datetime import datetime
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db


class Role(str, Enum):
    ADMIN = 'admin'
    LECTURER = 'lecturer'
    STUDENT = 'student'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    role = db.Column(db.Enum(Role, values_callable=lambda x: [e.value for e in x]),
                     nullable=False, default=Role.STUDENT)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    dark_mode = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    student_profile = db.relationship('Student', backref='user', uselist=False, cascade='all, delete-orphan')
    lecturer_profile = db.relationship('Lecturer', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_lecturer(self):
        return self.role == Role.LECTURER

    def is_student(self):
        return self.role == Role.STUDENT

    def __repr__(self):
        return f'<User {self.email}>'
