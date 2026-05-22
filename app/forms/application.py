from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class ApplicationForm(FlaskForm):
    programme_id = SelectField('Programme', coerce=int, validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(2, 64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(2, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    nationality = StringField('Nationality', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    education_background = TextAreaField('Education Background', validators=[DataRequired()])
    work_experience = TextAreaField('Work Experience', validators=[Optional()])
    document = FileField('ID Document', validators=[FileAllowed(['pdf', 'jpg', 'jpeg', 'png'])])
    transcript = FileField('Transcript/Certificate', validators=[FileAllowed(['pdf'])])
    submit = SubmitField('Submit Application')


class ApplicationTrackForm(FlaskForm):
    tracking_id = StringField('Tracking ID', validators=[DataRequired()])
    submit = SubmitField('Track Application')
