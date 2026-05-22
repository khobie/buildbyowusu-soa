from flask import render_template, current_app
from flask_mail import Message
from app import mail


def send_email(to, subject, template, **kwargs):
    if not current_app.config.get('MAIL_USERNAME'):
        return False
    try:
        msg = Message(
            subject=subject,
            recipients=[to] if isinstance(to, str) else to,
            html=render_template(f'email/{template}', **kwargs),
        )
        mail.send(msg)
        return True
    except Exception:
        return False
