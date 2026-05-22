from app.models.user import User, Role
from app.models.student import Student
from app.models.lecturer import Lecturer
from app.models.department import Department
from app.models.programme import Programme, Course
from app.models.academic import Result, Timetable, CourseMaterial, Assignment, AssignmentSubmission
from app.models.clinical import ClinicalPosting, Attendance
from app.models.application import Application
from app.models.content import Announcement, News, Event, GalleryImage, Testimonial, PartnerHospital
from app.models.faculty import FacultyMember

__all__ = [
    'User', 'Role', 'Student', 'Lecturer', 'Department', 'Programme', 'Course',
    'Result', 'Timetable', 'CourseMaterial', 'Assignment', 'AssignmentSubmission',
    'ClinicalPosting', 'Attendance', 'Application', 'Announcement', 'News', 'Event',
    'GalleryImage', 'Testimonial', 'PartnerHospital', 'FacultyMember',
]
