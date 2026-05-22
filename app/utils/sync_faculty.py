from sqlalchemy import inspect, text
from app import db
from app.models import FacultyMember
from app.utils.faculty_data import ADMINISTRATION_TEAM, ACADEMIC_FACULTY, DIRECTOR_RECORD


def _ensure_category_column():
    """Add category column to existing databases."""
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns('faculty_members')]
    if 'category' not in columns:
        with db.engine.connect() as conn:
            conn.execute(text(
                "ALTER TABLE faculty_members ADD COLUMN category VARCHAR(30) DEFAULT 'academic'"
            ))
            conn.commit()


def sync_faculty_team():
    """Refresh administration and academic team lists."""
    _ensure_category_column()

    FacultyMember.query.delete()

    name, title, spec, photo, order, category = DIRECTOR_RECORD
    db.session.add(FacultyMember(
        name=name, title=title, specialization=spec, photo=photo,
        display_order=order, category=category,
    ))

    for name, title, spec, order in ADMINISTRATION_TEAM:
        db.session.add(FacultyMember(
            name=name, title=title, specialization=spec,
            category='administration', display_order=order,
        ))

    for name, title, spec, order in ACADEMIC_FACULTY:
        db.session.add(FacultyMember(
            name=name, title=title, specialization=spec,
            category='academic', display_order=order,
        ))

    db.session.commit()
