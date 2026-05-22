from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func
from app import db
from app.models import (
    User, Role, Student, Lecturer, Programme, Course, Department,
    Application, Announcement, ClinicalPosting, Result, News, Event,
)
from app.forms import (
    AnnouncementForm, ProgrammeForm, StudentForm, LecturerForm,
    ResultForm, ClinicalPostingForm, NewsForm, EventForm, DepartmentForm,
)
from app.utils.decorators import admin_required, lecturer_required
from app.utils.files import save_upload
from app.utils.reports import export_csv
from app.utils.qr import generate_student_qr
import re

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
@login_required
@lecturer_required
def dashboard():
    stats = {
        'students': Student.query.count(),
        'lecturers': Lecturer.query.count(),
        'applications': Application.query.filter_by(status='pending').count(),
        'announcements': Announcement.query.count(),
        'postings': ClinicalPosting.query.filter_by(status='active').count(),
        'total_applications': Application.query.count(),
    }
    recent_apps = Application.query.order_by(Application.submitted_at.desc()).limit(5).all()
    recent_announcements = Announcement.query.order_by(Announcement.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html',
        stats=stats, recent_apps=recent_apps, recent_announcements=recent_announcements)


# --- Students ---
@admin_bp.route('/students')
@login_required
@admin_required
def students():
    page = request.args.get('page', 1, type=int)
    pagination = Student.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/students.html', pagination=pagination)


@admin_bp.route('/students/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_student():
    form = StudentForm()
    form.programme_id.choices = [(0, '-- Select --')] + [(p.id, p.name) for p in Programme.query.all()]
    form.department_id.choices = [(0, '-- Select --')] + [(d.id, d.name) for d in Department.query.all()]
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=Role.STUDENT,
        )
        user.set_password(form.password.data or 'Student@2024!')
        db.session.add(user)
        db.session.flush()
        student = Student(
            user_id=user.id,
            student_id=form.student_id.data,
            programme_id=form.programme_id.data or None,
            department_id=form.department_id.data or None,
            year_of_study=form.year_of_study.data,
        )
        db.session.add(student)
        db.session.flush()
        student.qr_code_path = generate_student_qr(student)
        db.session.commit()
        flash('Student created.', 'success')
        return redirect(url_for('admin.students'))
    return render_template('admin/student_form.html', form=form, title='Add Student')


# --- Lecturers ---
@admin_bp.route('/lecturers')
@login_required
@admin_required
def lecturers():
    all_lecturers = Lecturer.query.all()
    return render_template('admin/lecturers.html', lecturers=all_lecturers)


@admin_bp.route('/lecturers/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lecturer():
    form = LecturerForm()
    form.department_id.choices = [(0, '-- Select --')] + [(d.id, d.name) for d in Department.query.all()]
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=Role.LECTURER,
        )
        user.set_password(form.password.data or 'Lecturer@2024!')
        db.session.add(user)
        db.session.flush()
        lecturer = Lecturer(
            user_id=user.id,
            staff_id=form.staff_id.data,
            department_id=form.department_id.data or None,
            title=form.title.data,
            specialization=form.specialization.data,
        )
        db.session.add(lecturer)
        db.session.commit()
        flash('Lecturer created.', 'success')
        return redirect(url_for('admin.lecturers'))
    return render_template('admin/lecturer_form.html', form=form, title='Add Lecturer')


# --- Applications ---
@admin_bp.route('/applications')
@login_required
@admin_required
def applications():
    status = request.args.get('status', 'pending')
    apps = Application.query.filter_by(status=status).order_by(Application.submitted_at.desc()).all()
    return render_template('admin/applications.html', applications=apps, status=status)


@admin_bp.route('/applications/<int:id>/<action>')
@login_required
@admin_required
def application_action(id, action):
    app_record = Application.query.get_or_404(id)
    if action in ('approve', 'reject', 'review'):
        app_record.status = action if action != 'review' else 'under_review'
        app_record.reviewed_at = datetime.utcnow()
        db.session.commit()
        flash(f'Application {action}d.', 'success')
    return redirect(url_for('admin.applications'))


# --- Announcements ---
@admin_bp.route('/announcements', methods=['GET', 'POST'])
@login_required
@lecturer_required
def manage_announcements():
    form = AnnouncementForm()
    if form.validate_on_submit():
        ann = Announcement(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            show_ticker=form.show_ticker.data,
            is_published=form.is_published.data,
            author_id=current_user.id,
        )
        db.session.add(ann)
        db.session.commit()
        flash('Announcement published.', 'success')
        return redirect(url_for('admin.manage_announcements'))
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return render_template('admin/announcements.html', form=form, announcements=announcements)


# --- Programmes ---
@admin_bp.route('/programmes', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_programmes():
    form = ProgrammeForm()
    form.department_id.choices = [(0, '-- Select --')] + [(d.id, d.name) for d in Department.query.all()]
    if form.validate_on_submit():
        prog = Programme(
            name=form.name.data, code=form.code.data, level=form.level.data,
            duration=form.duration.data, description=form.description.data,
            entry_requirements=form.entry_requirements.data,
            tuition_fee=form.tuition_fee.data,
            curriculum=form.curriculum.data,
            clinical_structure=form.clinical_structure.data,
            department_id=form.department_id.data or None,
            is_featured=form.is_featured.data,
        )
        db.session.add(prog)
        db.session.commit()
        flash('Programme added.', 'success')
        return redirect(url_for('admin.manage_programmes'))
    programmes = Programme.query.all()
    return render_template('admin/programmes.html', form=form, programmes=programmes)


# --- Results ---
@admin_bp.route('/results', methods=['GET', 'POST'])
@login_required
@lecturer_required
def manage_results():
    form = ResultForm()
    form.student_id.choices = [(s.id, f'{s.student_id} - {s.user.full_name}') for s in Student.query.all()]
    form.course_id.choices = [(c.id, c.title) for c in Course.query.all()]
    if form.validate_on_submit():
        cw = form.coursework_score.data or 0
        ex = form.exam_score.data or 0
        total = cw * 0.4 + ex * 0.6
        result = Result(
            student_id=form.student_id.data,
            course_id=form.course_id.data,
            semester=form.semester.data,
            academic_year=form.academic_year.data,
            coursework_score=cw, exam_score=ex,
            total_score=round(total, 1),
            grade=form.grade.data or _calc_grade(total),
            published=True,
        )
        db.session.add(result)
        db.session.commit()
        flash('Result uploaded.', 'success')
        return redirect(url_for('admin.manage_results'))
    results_list = Result.query.order_by(Result.created_at.desc()).limit(50).all()
    return render_template('admin/results.html', form=form, results=results_list)


def _calc_grade(score):
    if score >= 80: return 'A'
    if score >= 70: return 'B'
    if score >= 60: return 'C'
    if score >= 50: return 'D'
    return 'F'


# --- Clinical ---
@admin_bp.route('/clinical', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_clinical():
    form = ClinicalPostingForm()
    form.student_id.choices = [(s.id, s.student_id) for s in Student.query.all()]
    form.supervisor_id.choices = [(0, '-- None --')] + [
        (l.id, l.user.full_name) for l in Lecturer.query.all()
    ]
    if form.validate_on_submit():
        posting = ClinicalPosting(
            student_id=form.student_id.data,
            hospital_name=form.hospital_name.data,
            department_unit=form.department_unit.data,
            posting_type=form.posting_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            supervisor_id=form.supervisor_id.data or None,
            status='active',
        )
        db.session.add(posting)
        db.session.commit()
        flash('Clinical posting created.', 'success')
        return redirect(url_for('admin.manage_clinical'))
    postings = ClinicalPosting.query.order_by(ClinicalPosting.start_date.desc()).all()
    return render_template('admin/clinical.html', form=form, postings=postings)


# --- Departments ---
@admin_bp.route('/departments', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_departments():
    form = DepartmentForm()
    if form.validate_on_submit():
        dept = Department(
            name=form.name.data, code=form.code.data,
            description=form.description.data, head_name=form.head_name.data,
        )
        db.session.add(dept)
        db.session.commit()
        flash('Department added.', 'success')
        return redirect(url_for('admin.manage_departments'))
    departments = Department.query.all()
    return render_template('admin/departments.html', form=form, departments=departments)


# --- News & Events ---
@admin_bp.route('/news', methods=['GET', 'POST'])
@login_required
@lecturer_required
def manage_news():
    form = NewsForm()
    if form.validate_on_submit():
        slug = re.sub(r'[^a-z0-9]+', '-', form.title.data.lower()).strip('-')
        article = News(
            title=form.title.data, slug=slug, summary=form.summary.data,
            content=form.content.data, is_published=form.is_published.data,
            author_id=current_user.id,
        )
        if form.image.data:
            article.image = save_upload(form.image.data, 'gallery')
        db.session.add(article)
        db.session.commit()
        flash('News article published.', 'success')
        return redirect(url_for('admin.manage_news'))
    articles = News.query.order_by(News.created_at.desc()).all()
    return render_template('admin/news.html', form=form, articles=articles)


@admin_bp.route('/events', methods=['GET', 'POST'])
@login_required
@lecturer_required
def manage_events():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data, description=form.description.data,
            event_type=form.event_type.data, location=form.location.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created.', 'success')
        return redirect(url_for('admin.manage_events'))
    events_list = Event.query.order_by(Event.start_datetime.desc()).all()
    return render_template('admin/events.html', form=form, events=events_list)


# --- Reports / Export ---
@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    return render_template('admin/reports.html')


@admin_bp.route('/export/students')
@login_required
@admin_required
def export_students():
    rows = []
    for s in Student.query.all():
        rows.append([s.student_id, s.user.full_name, s.user.email,
                     s.programme.name if s.programme else '', s.status])
    return export_csv('students.csv',
        ['Student ID', 'Name', 'Email', 'Programme', 'Status'], rows)


@admin_bp.route('/export/applications')
@login_required
@admin_required
def export_applications():
    rows = [[a.tracking_id, f'{a.first_name} {a.last_name}', a.email,
             a.programme.name if a.programme else '', a.status, a.submitted_at]
            for a in Application.query.all()]
    return export_csv('applications.csv',
        ['Tracking ID', 'Name', 'Email', 'Programme', 'Status', 'Submitted'], rows)
