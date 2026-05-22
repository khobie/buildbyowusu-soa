from app import db


class FacultyMember(db.Model):
    __tablename__ = 'faculty_members'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100))
    specialization = db.Column(db.String(150))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))
    email = db.Column(db.String(120))
    category = db.Column(db.String(30), default='academic', index=True)
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)

    @property
    def is_administration(self):
        return self.category == 'administration'

    @property
    def is_academic(self):
        return self.category == 'academic'
