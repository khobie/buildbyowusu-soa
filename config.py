import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:postgres@localhost:5432/ridge_anaesthesia'
    )
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgres://', 'postgresql://', 1
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_pre_ping': True}

    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}

    WTF_CSRF_ENABLED = True
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@ridgeanaesthesia.edu')

    SCHOOL_NAME = 'Ridge School of Anaesthesia'
    SCHOOL_MOTTO = 'Excellence in Anaesthetic Practice & Patient Safety'
    SCHOOL_AFFILIATION = 'University of Cape Coast (UCC)'
    SCHOOL_AFFILIATION_SHORT = 'Affiliated to UCC'
    SCHOOL_LOGO = 'img/logos/soa-logo.png'
    # Paths relative to app/static/ — sync from IMAGES/ via: flask --app run sync-images
    SITE_IMAGES = {
        'logo': 'img/logos/soa-logo.png',
        'hero': 'img/hero/surgery.jpg',
        'about': 'img/about/classroom.jpg',
        'clinical': 'img/hero/surgery.jpg',
        'director': 'img/faculty/director.jpeg',
    }
    LIBRARY_URL = os.environ.get('LIBRARY_URL', 'https://soal.librarika.com/')
    STUDENT_PORTAL_URL = os.environ.get('STUDENT_PORTAL_URL', 'https://soa.edu.gh/portal/login')
    DIRECTOR_NAME = 'Prof. James Ridge'
    DIRECTOR_TITLE = 'Director / Dean & Consultant Anaesthetist'
    DIRECTOR_WELCOME = (
        'It is my privilege to welcome you to the Ridge School of Anaesthesia — an institution '
        'dedicated to shaping skilled, compassionate, and safety-conscious anaesthesia professionals '
        'for Ghana and beyond.\n\n'
        'Since our establishment in 2008, we have remained committed to one clear purpose: to deliver '
        'the BSc in Anaesthesia with the highest standards of academic rigour and hands-on clinical '
        'experience. Our affiliation with the University of Cape Coast (UCC) strengthens that commitment, '
        'ensuring that every graduate leaves our programme prepared not only for the operating theatre '
        'and the intensive care unit, but for a lifetime of ethical and evidence-based practice.\n\n'
        'At Ridge, learning extends far beyond the classroom. Through structured rotations at our partner '
        'teaching hospitals, simulation-based training, and close mentorship from experienced consultants '
        'and lecturers, our students develop the confidence and competence that patients and surgical teams '
        'rightfully expect. We take pride in a learning environment that is disciplined, supportive, and '
        'deeply rooted in patient safety.\n\n'
        'Whether you are a prospective student exploring admission, a clinical partner supporting our '
        'training mission, or a member of our alumni community, I invite you to discover what makes Ridge '
        'distinct: excellence in anaesthetic practice, integrity in professional conduct, and an unwavering '
        'focus on the lives entrusted to our care.\n\n'
        'Thank you for visiting. We look forward to walking this journey with you.'
    )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ridge_anaesthesia.db')
    )


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgres://', 'postgresql://', 1
        )


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig,
}
