import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

from config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    for sub in ('documents', 'lectures', 'gallery', 'applications', 'profiles'):
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], sub), exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.session_protection = 'strong'

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.main import main_bp
    from app.auth.routes import auth_bp
    from app.student.routes import student_bp
    from app.admin.routes import admin_bp
    from app.api.routes import api_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.context_processor
    def inject_globals():
        from datetime import datetime
        return {
            'school_name': app.config.get('SCHOOL_NAME'),
            'school_motto': app.config.get('SCHOOL_MOTTO'),
            'school_affiliation': app.config.get('SCHOOL_AFFILIATION'),
            'school_affiliation_short': app.config.get('SCHOOL_AFFILIATION_SHORT'),
            'director_name': app.config.get('DIRECTOR_NAME'),
            'director_title': app.config.get('DIRECTOR_TITLE'),
            'director_welcome': app.config.get('DIRECTOR_WELCOME'),
            'current_year': datetime.utcnow().year,
            'school_logo': app.config.get('SCHOOL_LOGO'),
            'site_images': app.config.get('SITE_IMAGES', {}),
            'library_url': app.config.get('LIBRARY_URL'),
            'student_portal_url': app.config.get('STUDENT_PORTAL_URL'),
        }

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template('errors/404.html'), 404

    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template('errors/403.html'), 403

    return app
