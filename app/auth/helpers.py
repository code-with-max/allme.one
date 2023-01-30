from flask import url_for, flash, render_template
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature
from smtplib import SMTPServerDisconnected
from app.extensions import mail
from app.auth import s  # FIXME I think need another variable name
from config import Config


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
        msg_body_template = 'mail/email_confirmation.html'
    elif action == 'reset':
        url_endpoint = 'auth.do_password_reset'
        msg_subject = 'Forgotten password reset'
        msg_body_template = 'mail/password_reset.html'

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
