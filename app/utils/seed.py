from datetime import datetime
from app import db
from app.models import (
    User, Role, Student, Lecturer, Department, Programme, Course,
    Announcement, News, Event, Testimonial, PartnerHospital, FacultyMember,
    Application,
)

BSC_PROGRAMME = {
    'name': 'BSc in Anaesthesia',
    'code': 'BSC-ANA',
    'level': 'Undergraduate',
    'duration': '4 Years',
    'is_featured': True,
    'description': (
        'The Bachelor of Science in Anaesthesia is our flagship programme, '
        'combining rigorous academic study with extensive clinical training in '
        'operating theatres, ICU, and critical care settings.'
    ),
    'entry_requirements': (
        'WASSCE/SSCE with credits in English, Mathematics, Biology, Chemistry, and Physics. '
        'Aggregate 14 or better. Mature applicants may be considered with relevant clinical experience.'
    ),
    'tuition_fee': 'GHS 12,000 per academic year',
    'curriculum': (
        'Year 1: Foundations of Anaesthesia, Human Physiology, Pharmacology, Professional Ethics. '
        'Year 2: Airway Management, Regional Anaesthesia, Clinical Practice I. '
        'Year 3: Critical Care, Paediatric & Obstetric Anaesthesia, Research Methods. '
        'Year 4: Advanced Clinical Practice, Pain Management, Dissertation.'
    ),
    'clinical_structure': (
        'Progressive hospital rotations across partner institutions: General Theatre, ICU, '
        'Recovery, Paediatric Anaesthesia, and specialty units with assigned supervisors.'
    ),
}

BSC_COURSES = [
    ('ANA101', 'Introduction to Anaesthesia', 1, 1),
    ('ANA102', 'Anaesthetic Pharmacology', 1, 1),
    ('ANA201', 'Airway & Regional Anaesthesia', 2, 1),
    ('ANA301', 'Advanced Airway Management', 3, 1),
    ('ANA401', 'Critical Care Anaesthesia', 4, 2),
]


def ensure_bsc_only():
    """Ensure only BSc in Anaesthesia is offered; remove legacy diploma programme."""
    dept = Department.query.first()
    if not dept:
        dept = Department(name='Department of Anaesthesia', code='ANA', head_name='Prof. James Ridge')
        db.session.add(dept)
        db.session.flush()

    bsc = Programme.query.filter_by(code='BSC-ANA').first()
    if not bsc:
        bsc = Programme(department_id=dept.id, **BSC_PROGRAMME)
        db.session.add(bsc)
        db.session.flush()
    else:
        for key, value in BSC_PROGRAMME.items():
            setattr(bsc, key, value)
        bsc.department_id = dept.id

    dip = Programme.query.filter_by(code='DIP-ANA').first()
    if dip:
        Application.query.filter_by(programme_id=dip.id).update({'programme_id': bsc.id})
        Student.query.filter_by(programme_id=dip.id).update({'programme_id': bsc.id})
        Course.query.filter_by(programme_id=dip.id).delete()
        db.session.delete(dip)

    if not Course.query.filter_by(programme_id=bsc.id).first():
        for code, title, year, sem in BSC_COURSES:
            db.session.add(Course(
                programme_id=bsc.id, code=code, title=title,
                year=year, semester=sem, credits=3,
            ))

    Programme.query.filter(Programme.code != 'BSC-ANA').update(
        {'is_featured': False}, synchronize_session=False
    )
    bsc.is_featured = True

    from app.utils.sync_faculty import sync_faculty_team
    sync_faculty_team()

    for ann in Announcement.query.filter(Announcement.content.ilike('%Diploma%')).all():
        ann.content = ann.content.replace(
            'Diploma and BSc programmes', 'BSc in Anaesthesia'
        ).replace('Diploma and BSc', 'BSc in Anaesthesia')

    db.session.commit()
    return bsc


def seed_all():
    if Department.query.first():
        ensure_bsc_only()
        return

    dept = Department(name='Department of Anaesthesia', code='ANA', head_name='Prof. James Ridge')
    db.session.add(dept)
    db.session.flush()

    bsc = Programme(department_id=dept.id, **BSC_PROGRAMME)
    db.session.add(bsc)
    db.session.flush()

    for code, title, year, sem in BSC_COURSES:
        db.session.add(Course(
            programme_id=bsc.id, code=code, title=title,
            year=year, semester=sem, credits=3,
        ))

    testimonials = [
        ('Dr. Ama Mensah', 'Consultant Anaesthetist, Ridge Medical Centre',
         'Ridge School transformed my clinical confidence. The ICU rotations were world-class.'),
        ('Kwesi Boateng', 'BSc in Anaesthesia Graduate, 2024',
         'The faculty dedication and hospital partnerships gave me real theatre experience from year one.'),
        ('Dr. Sarah Osei', 'ICU Specialist',
         'As a supervisor, I have seen Ridge trainees consistently exceed expectations in critical care settings.'),
    ]
    for name, role, content in testimonials:
        db.session.add(Testimonial(name=name, role=role, content=content, rating=5))

    hospitals = [
        ('Ridge Medical Centre', 'Accra', 'teaching'),
        ('Korle Bu Teaching Hospital', 'Accra', 'clinical'),
        ('37 Military Hospital', 'Accra', 'clinical'),
        ('Komfo Anokye Teaching Hospital', 'Kumasi', 'rotation'),
    ]
    for name, loc, ptype in hospitals:
        db.session.add(PartnerHospital(name=name, location=loc, partnership_type=ptype))

    from app.utils.sync_faculty import sync_faculty_team
    sync_faculty_team()

    db.session.add(Announcement(
        title='2025/2026 Admissions Now Open',
        content='Applications for BSc in Anaesthesia (Affiliated to UCC) are now being accepted. Deadline: August 31, 2025.',
        category='academic', show_ticker=True, is_published=True,
    ))
    db.session.add(Announcement(
        title='ICU Simulation Workshop',
        content='Mandatory workshop for Year 2 students on June 15, 2025 at Ridge Simulation Centre.',
        category='clinical', show_ticker=True, is_published=True,
    ))

    db.session.add(News(
        title='Ridge School Affiliated to University of Cape Coast',
        slug='ridge-school-affiliated-to-ucc',
        summary='Ridge School of Anaesthesia is affiliated to UCC for the BSc in Anaesthesia.',
        content='Ridge School of Anaesthesia is proudly affiliated to the University of Cape Coast (UCC). Our BSc in Anaesthesia is delivered under this academic partnership.',
        is_published=True,
    ))

    db.session.add(Event(
        title='Annual Anaesthesia Conference 2025',
        description='Regional conference on advances in anaesthetic practice.',
        event_type='conference', location='Ridge Conference Hall',
        start_datetime=datetime(2025, 9, 20, 9, 0),
        end_datetime=datetime(2025, 9, 22, 17, 0),
    ))

    if not User.query.filter_by(email='student@ridgeanaesthesia.edu').first():
        user = User(
            email='student@ridgeanaesthesia.edu', first_name='Kofi', last_name='Mensah',
            role=Role.STUDENT, phone='+233 24 000 0001',
        )
        user.set_password('Student@2024!')
        db.session.add(user)
        db.session.flush()
        db.session.add(Student(
            user_id=user.id, student_id='RSA2024001',
            programme_id=bsc.id, department_id=dept.id, year_of_study=2,
        ))

    db.session.commit()
