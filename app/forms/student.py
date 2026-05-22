from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional, Length


class ProfileUpdateForm(FlaskForm):
    phone = StringField('Phone')
    address = TextAreaField('Address')
    emergency_contact = StringField('Emergency Contact')
    emergency_phone = StringField('Emergency Phone')
    avatar = FileField('Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update Profile')


class AssignmentSubmitForm(FlaskForm):
    notes = TextAreaField('Notes', validators=[Optional()])
    file = FileField('Submission File', validators=[DataRequired(), FileAllowed(['pdf', 'doc', 'docx'])])
    submit = SubmitField('Submit Assignment')
