from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import Student, Lecturer, Application, Announcement, ClinicalPosting
from app.utils.decorators import admin_required

api_bp = Blueprint('api', __name__)


@api_bp.route('/stats')
@login_required
@admin_required
def stats():
    return jsonify({
        'students': Student.query.count(),
        'lecturers': Lecturer.query.count(),
        'pending_applications': Application.query.filter_by(status='pending').count(),
        'announcements': Announcement.query.count(),
        'active_postings': ClinicalPosting.query.filter_by(status='active').count(),
    })


@api_bp.route('/announcements')
def announcements_feed():
    from app.models import Announcement
    items = Announcement.query.filter_by(is_published=True, show_ticker=True)\
        .order_by(Announcement.created_at.desc()).limit(10).all()
    return jsonify([{'title': a.title, 'content': a.content[:100]} for a in items])
