"""One-time / startup database setup for production (e.g. Render free tier)."""
from app import db
from app.models import User, Role, Programme


def ensure_database():
    """Create tables, default admin, and seed if the database is empty."""
    db.create_all()

    if not User.query.filter_by(email='admin@ridgeanaesthesia.edu').first():
        admin = User(
            email='admin@ridgeanaesthesia.edu',
            first_name='System',
            last_name='Administrator',
            role=Role.ADMIN,
            is_active=True,
        )
        admin.set_password('Admin@2024!')
        db.session.add(admin)

    if not Programme.query.first():
        db.session.flush()
        from app.utils.seed import seed_all
        seed_all()
    elif db.session.new or db.session.dirty:
        db.session.commit()
