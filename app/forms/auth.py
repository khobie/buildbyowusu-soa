from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(2, 64)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(2, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone')
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered.')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')


class PasswordResetConfirmForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(8, 128)])
    confirm_password = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
