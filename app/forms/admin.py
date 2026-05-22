from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, SelectField, DateField, DateTimeField, FloatField, BooleanField, SubmitField, IntegerField, TimeField
from wtforms.validators import DataRequired, Email, Optional, Length


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(5, 200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('general', 'General'), ('academic', 'Academic'), ('clinical', 'Clinical'), ('event', 'Event'),
    ])
    show_ticker = BooleanField('Show on Ticker')
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save')


class ProgrammeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    level = StringField('Level')
    duration = StringField('Duration')
    description = TextAreaField('Description')
    entry_requirements = TextAreaField('Entry Requirements')
    tuition_fee = StringField('Tuition Fee')
    curriculum = TextAreaField('Curriculum')
    clinical_structure = TextAreaField('Clinical Structure')
    department_id = SelectField('Department', coerce=int, validators=[Optional()])
    is_featured = BooleanField('Featured')
    submit = SubmitField('Save')


class StudentForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    student_id = StringField('Student ID', validators=[DataRequired()])
    programme_id = SelectField('Programme', coerce=int, validators=[Optional()])
    department_id = SelectField('Department', coerce=int, validators=[Optional()])
    year_of_study = IntegerField('Year', default=1)
    password = StringField('Password', validators=[Optional()])
    submit = SubmitField('Save')


class LecturerForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    staff_id = StringField('Staff ID', validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[Optional()])
    title = StringField('Title')
    specialization = StringField('Specialization')
    password = StringField('Password', validators=[Optional()])
    submit = SubmitField('Save')


class ResultForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    semester = StringField('Semester', validators=[DataRequired()])
    academic_year = StringField('Academic Year', validators=[DataRequired()])
    coursework_score = FloatField('Coursework', validators=[Optional()])
    exam_score = FloatField('Exam', validators=[Optional()])
    grade = StringField('Grade')
    submit = SubmitField('Save')


class ClinicalPostingForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    hospital_name = StringField('Hospital', validators=[DataRequired()])
    department_unit = StringField('Unit')
    posting_type = SelectField('Type', choices=[
        ('icu', 'ICU'), ('theatre', 'Theatre'), ('ward', 'Ward'), ('recovery', 'Recovery'),
    ])
    start_date = DateField('Start', validators=[DataRequired()])
    end_date = DateField('End', validators=[DataRequired()])
    supervisor_id = SelectField('Supervisor', coerce=int, validators=[Optional()])
    submit = SubmitField('Save')


class NewsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary')
    content = TextAreaField('Content', validators=[DataRequired()])
    image = FileField('Image')
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save')


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    event_type = SelectField('Type', choices=[
        ('seminar', 'Seminar'), ('workshop', 'Workshop'), ('conference', 'Conference'), ('other', 'Other'),
    ])
    location = StringField('Location')
    start_datetime = DateTimeField('Start', validators=[DataRequired()])
    end_datetime = DateTimeField('End', validators=[Optional()])
    submit = SubmitField('Save')


class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    description = TextAreaField('Description')
    head_name = StringField('Head of Department')
    submit = SubmitField('Save')
