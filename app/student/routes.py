from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, current_app
from flask_login import login_required, current_user
from app import db
from app.models import (
    Announcement, Result, Timetable, CourseMaterial, Assignment,
    AssignmentSubmission, ClinicalPosting,
)
from app.forms import ProfileUpdateForm, AssignmentSubmitForm
from app.utils.decorators import student_required
from app.utils.files import save_upload

student_bp = Blueprint('student', __name__)


def _get_student():
    return current_user.student_profile


@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    student = _get_student()
    announcements = Announcement.query.filter_by(is_published=True).order_by(
        Announcement.created_at.desc()
    ).limit(5).all()
    postings = student.clinical_postings.order_by(ClinicalPosting.start_date.desc()).limit(3).all()
    pending_assignments = Assignment.query.join(
        AssignmentSubmission, isouter=True
    ).filter(
        (AssignmentSubmission.id == None) | (AssignmentSubmission.student_id != student.id)
    ).limit(5).all()
    return render_template('student/dashboard.html',
        student=student, announcements=announcements,
        postings=postings, pending_assignments=pending_assignments)


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    student = _get_student()
    form = ProfileUpdateForm(obj=student)
    if form.validate_on_submit():
        current_user.phone = form.phone.data
        student.address = form.address.data
        student.emergency_contact = form.emergency_contact.data
        student.emergency_phone = form.emergency_phone.data
        if form.avatar.data:
            path = save_upload(form.avatar.data, 'profiles')
            if path:
                current_user.avatar = path
        db.session.commit()
        flash('Profile updated.', 'success')
        return redirect(url_for('student.profile'))
    return render_template('student/profile.html', student=student, form=form)


@student_bp.route('/results')
@login_required
@student_required
def results():
    student = _get_student()
    results_list = student.results.filter_by(published=True).all()
    return render_template('student/results.html', results=results_list)


@student_bp.route('/timetable')
@login_required
@student_required
def timetable():
    student = _get_student()
    entries = Timetable.query.filter_by(programme_id=student.programme_id).order_by(
        Timetable.day_of_week, Timetable.start_time
    ).all()
    return render_template('student/timetable.html', entries=entries)


@student_bp.route('/materials')
@login_required
@student_required
def materials():
    student = _get_student()
    if student.programme_id:
        from app.models import Course
        course_ids = [c.id for c in Course.query.filter_by(programme_id=student.programme_id).all()]
        materials_list = CourseMaterial.query.filter(CourseMaterial.course_id.in_(course_ids)).all()
    else:
        materials_list = []
    return render_template('student/materials.html', materials=materials_list)


@student_bp.route('/materials/download/<int:id>')
@login_required
@student_required
def download_material(id):
    material = CourseMaterial.query.get_or_404(id)
    folder = current_app.config['UPLOAD_FOLDER']
    filename = material.file_path.split('/')[-1]
    subfolder = material.file_path.split('/')[1] if '/' in material.file_path else 'lectures'
    return send_from_directory(
        f'{folder}/{subfolder}', filename, as_attachment=True
    )


@student_bp.route('/announcements')
@login_required
@student_required
def announcements():
    items = Announcement.query.filter_by(is_published=True).order_by(
        Announcement.created_at.desc()
    ).all()
    return render_template('student/announcements.html', announcements=items)


@student_bp.route('/clinical')
@login_required
@student_required
def clinical():
    student = _get_student()
    postings = student.clinical_postings.order_by(ClinicalPosting.start_date.desc()).all()
    return render_template('student/clinical.html', postings=postings)


@student_bp.route('/assignments')
@login_required
@student_required
def assignments():
    student = _get_student()
    all_assignments = Assignment.query.order_by(Assignment.due_date.desc()).all()
    submissions = {s.assignment_id: s for s in student.submissions.all()}
    return render_template('student/assignments.html',
        assignments=all_assignments, submissions=submissions)


@student_bp.route('/assignments/<int:id>/submit', methods=['GET', 'POST'])
@login_required
@student_required
def submit_assignment(id):
    student = _get_student()
    assignment = Assignment.query.get_or_404(id)
    form = AssignmentSubmitForm()
    existing = AssignmentSubmission.query.filter_by(
        assignment_id=id, student_id=student.id
    ).first()
    if form.validate_on_submit():
        path = save_upload(form.file.data, 'documents')
        if existing:
            existing.file_path = path
            existing.notes = form.notes.data
            existing.status = 'submitted'
        else:
            sub = AssignmentSubmission(
                assignment_id=id, student_id=student.id,
                file_path=path, notes=form.notes.data,
            )
            db.session.add(sub)
        db.session.commit()
        flash('Assignment submitted.', 'success')
        return redirect(url_for('student.assignments'))
    return render_template('student/submit_assignment.html',
        assignment=assignment, form=form, existing=existing)


@student_bp.route('/id-card')
@login_required
@student_required
def id_card():
    student = _get_student()
    return render_template('student/id_card.html', student=student)
