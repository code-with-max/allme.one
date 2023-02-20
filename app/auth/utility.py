from flask import url_for, redirect, flash, render_template
from flask_mail import Message
from flask_login import current_user
from itsdangerous import SignatureExpired, BadTimeSignature
from smtplib import SMTPServerDisconnected
from app.extensions import mail
from app.auth import s  # FIXME I think need another variable name
from config import Config
from functools import wraps


def send_verification_email(email_adress: str, action: str) -> bool:
    '''
    Sending email with email confirmation or password reset links :)\n
    Use:\n
    send_verification_email('<email>', 'confirm') for confirmation \n
    send_verification_email('<email>', 'reset') for password reset\n
    '''
    if action == 'confirm':
        url_endpoint = 'auth.confirm_email'
        msg_subject = 'Email address confirmation'
        msg_body_template = 'mail/auth/email_confirmation.html'
    elif action == 'reset':
        url_endpoint = 'auth.do_password_reset'
        msg_subject = 'Forgotten password reset'
        msg_body_template = 'mail/auth/password_reset.html'

    salt = '3AB31D4935676'  # FIXME Must use env var
    token = s.dumps(email_adress, salt=salt)
    url = url_for(url_endpoint, token=token, _external=True)

    msg = Message(msg_subject,
                  sender="support@allme.one",  # FIXME Must use env var
                  recipients=[email_adress])
    msg.html = render_template(msg_body_template, confirm_url=url)
    try:
        mail.send(msg)
    except SMTPServerDisconnected:
        flash("It is not possible to send email", category='warning')
        return False
    except Exception as e:
        # TODO smtp server errors need to be handled
        # https://docs.python.org/3/library/smtplib.html
        flash("It is not possible to send email", category='warning')
        flash(str(e))
        return False
    else:
        flash("Email was send", category='success')
        return True


def validate_token(token: str) -> bool | str:
    '''
    Validate TTL confirmation links\n
    Return False if link not valid or confirmed e-mail (as str)
    '''
    salt = '3AB31D4935676'  # FIXME Must use env var
    try:
        email = s.loads(token, salt=salt, max_age=3600)
    except SignatureExpired:
        flash("Link expired", category='warning')
        return False
    except BadTimeSignature:
        flash("Link invalid", category='warning')
        return False
    else:
        # flash("Link approved", category='success')
        return email


def confirm_required(func):
    '''
    Check email confirmation decorator
    '''
    # FIXME its not work.
    # Cathed werkzeug.routing.exceptions.BuildError
    @wraps
    def wrapper(*args, **kwargs):
        if not current_user.email_confirmed:
            flash("Please, confirm you email", category='warning')
            return redirect(url_for("auth.email_not_confirmed"))
        return func(*args, **kwargs)
    return wrapper


def send_tech_letter(tech_data1, tech_data2, tech_data3):
    msg_subject = 'Technical report for geo IP'
    msg_body_template = 'mail/tech_data.html'
    msg = Message(msg_subject,
                  sender="support@allme.one", 
                  recipients=['max@deadend.xyz'])
    msg.html = render_template(msg_body_template,
                               report1=tech_data1,
                               report2=tech_data2,
                               report3=tech_data3,
                               )
    try:
        mail.send(msg)
    except Exception as e:
        return False
    else:
        return True
