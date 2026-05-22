from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from app import db
from app.models import (
    Programme, News, Announcement, Testimonial, PartnerHospital,
    Event, GalleryImage, FacultyMember, Application, CourseMaterial,
)
from app.forms import ApplicationForm, ApplicationTrackForm
from app.utils.files import save_upload
import secrets

main_bp = Blueprint('main', __name__)


@main_bp.route('/health')
def health():
    """Lightweight health check for Render (no database required)."""
    return {'status': 'ok'}, 200


@main_bp.route('/')
def index():
    programmes = Programme.query.filter_by(is_featured=True).limit(4).all()
    news = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).limit(3).all()
    announcements = Announcement.query.filter_by(is_published=True).order_by(Announcement.created_at.desc()).limit(4).all()
    testimonials = Testimonial.query.filter_by(is_active=True).limit(6).all()
    partners = PartnerHospital.query.filter_by(is_active=True).all()
    return render_template('public/index.html',
        programmes=programmes, news=news, announcements=announcements,
        testimonials=testimonials, partners=partners)


@main_bp.route('/about')
def about():
    administration = FacultyMember.query.filter_by(
        is_active=True, category='administration'
    ).order_by(FacultyMember.display_order).all()
    faculty = FacultyMember.query.filter_by(
        is_active=True, category='academic'
    ).order_by(FacultyMember.display_order).all()
    partners = PartnerHospital.query.filter_by(is_active=True).all()
    return render_template('public/about.html',
        administration=administration, faculty=faculty, partners=partners)


@main_bp.route('/programmes')
def programmes():
    all_programmes = Programme.query.order_by(Programme.name).all()
    return render_template('public/programmes.html', programmes=all_programmes)


@main_bp.route('/programmes/<int:id>')
def programme_detail(id):
    programme = Programme.query.get_or_404(id)
    return render_template('public/programme_detail.html', programme=programme)


@main_bp.route('/admissions', methods=['GET', 'POST'])
def admissions():
    form = ApplicationForm()
    track_form = ApplicationTrackForm()
    form.programme_id.choices = [(p.id, p.name) for p in Programme.query.all()]

    if form.validate_on_submit():
        tracking_id = f'RSA{secrets.token_hex(4).upper()}'
        app_record = Application(
            tracking_id=tracking_id,
            programme_id=form.programme_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            nationality=form.nationality.data,
            address=form.address.data,
            education_background=form.education_background.data,
            work_experience=form.work_experience.data,
        )
        if form.document.data:
            app_record.document_path = save_upload(form.document.data, 'applications')
        if form.transcript.data:
            app_record.transcript_path = save_upload(form.transcript.data, 'applications')
        db.session.add(app_record)
        db.session.commit()
        flash(f'Application submitted! Your tracking ID is: {tracking_id}', 'success')
        return redirect(url_for('main.admissions'))

    return render_template('public/admissions.html', form=form, track_form=track_form)


@main_bp.route('/admissions/track', methods=['POST'])
def track_application():
    track_form = ApplicationTrackForm()
    if track_form.validate_on_submit():
        app_record = Application.query.filter_by(tracking_id=track_form.tracking_id.data.upper()).first()
        if app_record:
            return render_template('public/application_status.html', application=app_record)
        flash('Application not found.', 'danger')
    return redirect(url_for('main.admissions'))


@main_bp.route('/news-events')
def news_events():
    articles = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).all()
    events_list = Event.query.filter_by(is_published=True).order_by(Event.start_datetime.desc()).all()
    return render_template('public/news_events.html', articles=articles, events=events_list)


@main_bp.route('/e-library')
def e_library():
    """Library information page — online catalog on Librarika (LIBRARY_URL)."""
    return render_template('public/e_library.html')


@main_bp.route('/news')
def news_list():
    articles = News.query.filter_by(is_published=True).order_by(News.created_at.desc()).all()
    return render_template('public/news.html', articles=articles)


@main_bp.route('/news/<slug>')
def news_detail(slug):
    article = News.query.filter_by(slug=slug, is_published=True).first_or_404()
    return render_template('public/news_detail.html', article=article)


@main_bp.route('/events')
def events():
    events_list = Event.query.filter_by(is_published=True).order_by(Event.start_datetime).all()
    return render_template('public/events.html', events=events_list)


@main_bp.route('/gallery')
def gallery():
    images = GalleryImage.query.order_by(GalleryImage.created_at.desc()).all()
    return render_template('public/gallery.html', images=images)


@main_bp.route('/clinical-training')
def clinical_training():
    return render_template('public/clinical_training.html')


@main_bp.route('/contact')
def contact():
    return render_template('public/contact.html')


@main_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    results = {'programmes': [], 'news': [], 'announcements': []}
    if q:
        results['programmes'] = Programme.query.filter(Programme.name.ilike(f'%{q}%')).limit(10).all()
        results['news'] = News.query.filter(News.title.ilike(f'%{q}%'), News.is_published == True).limit(10).all()
        results['announcements'] = Announcement.query.filter(
            Announcement.title.ilike(f'%{q}%'), Announcement.is_published == True
        ).limit(10).all()
    return render_template('public/search.html', q=q, results=results)


@main_bp.route('/brochure')
def brochure():
    return send_from_directory(
        current_app.static_folder, 'docs/admission_brochure.pdf',
        as_attachment=True, download_name='Ridge_Admissions_Brochure.pdf'
    )
