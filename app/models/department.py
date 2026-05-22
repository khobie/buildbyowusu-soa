from datetime import datetime
from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    description = db.Column(db.Text)
    head_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    programmes = db.relationship('Programme', backref='department', lazy='dynamic')

    def __repr__(self):
        return f'<Department {self.code}>'
