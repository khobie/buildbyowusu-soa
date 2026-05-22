from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from app import db
from app.models import User, Role
from app.forms import LoginForm, PasswordResetForm, PasswordResetConfirmForm
from app.utils.email import send_email

auth_bp = Blueprint('auth', __name__)


def _serializer():
    return URLSafeTimedSerializer(current_app.config['SECRET_KEY'])


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return _redirect_by_role()
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data) and user.is_active:
            login_user(user, remember=form.remember_me.data)
            user.last_login = datetime.utcnow()
            db.session.commit()
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return _redirect_by_role()
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', form=form)


def _redirect_by_role():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    if current_user.is_lecturer():
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('student.dashboard'))


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = _serializer().dumps(user.email, salt='password-reset')
            user.reset_token = token
            db.session.commit()
            reset_url = url_for('auth.reset_password_confirm', token=token, _external=True)
            send_email(user.email, 'Password Reset', 'reset_password.html', reset_url=reset_url, user=user)
        flash('If that email exists, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    form = PasswordResetConfirmForm()
    try:
        email = _serializer().loads(token, salt='password-reset', max_age=3600)
    except Exception:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(email=email).first_or_404()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.reset_token = None
        db.session.commit()
        flash('Password updated. You can now sign in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_confirm.html', form=form)


@auth_bp.route('/toggle-dark-mode', methods=['POST'])
@login_required
def toggle_dark_mode():
    current_user.dark_mode = not current_user.dark_mode
    db.session.commit()
    return redirect(request.referrer or url_for('main.index'))
