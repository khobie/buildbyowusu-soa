import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app, db
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG', 'development'))


@app.cli.command('init-db')
def init_db():
    """Initialize database and create default admin."""
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
        db.session.commit()
        print('Database initialized. Admin: admin@ridgeanaesthesia.edu / Admin@2024!')
    else:
        print('Database already initialized.')


@app.cli.command('seed')
def seed_data():
    """Seed sample data for demonstration."""
    from app.utils.seed import seed_all
    seed_all()
    print('Sample data seeded successfully.')


@app.cli.command('sync-programmes')
def sync_programmes():
    """Keep only BSc in Anaesthesia as the offered programme."""
    from app.utils.seed import ensure_bsc_only
    ensure_bsc_only()
    print('Programmes updated: BSc in Anaesthesia only.')


@app.cli.command('sync-faculty')
def sync_faculty():
    """Update administration and academic faculty lists."""
    from app.utils.sync_faculty import sync_faculty_team
    sync_faculty_team()
    print('Faculty team updated: Administration + Academic.')


@app.cli.command('sync-images')
def sync_images():
    """Copy images from IMAGES/ folder into app/static/img/."""
    from app.utils.sync_images import sync_images_from_folder
    copied = sync_images_from_folder()
    if copied:
        print('Synced images:', ', '.join(copied))
    else:
        print('No images found in IMAGES/. Add files to IMAGES/hero, logos, faculty, about.')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
