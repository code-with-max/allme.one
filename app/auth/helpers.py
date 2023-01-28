from flask import url_for, flash, render_template
from flask_mail import Message
from itsdangerous import SignatureExpired, BadTimeSignature
from smtplib import SMTPServerDisconnected
from app.extensions import mail
from app.auth import s  # FIXME I think need another variable name
from config import Config


def send_verification_email(email_adress):
    '''
    Sending email with verification link :)
    '''
    token = s.dumps(email_adress, salt='confirm')  # FIXME Must use env var
    url = url_for('auth.confirm_email', token=token, _external=True)
    # print("***")
    # print(link)
    # print("***")
    msg = Message("Email confirmation",
                  sender="support@allme.one",
                  recipients=[email_adress])
    msg.html = render_template('mail/email_confirmation.html', confirm_url=url)
    try:
        mail.send(msg)
    except SMTPServerDisconnected:
        flash("It is not possible to send a confirmation email", category='warning')
        return False
    except Exception as e:
        # TODO Errors need to be handled https://docs.python.org/3/library/smtplib.html
        flash("It is not possible to send a confirmation email", category='warning')
        flash(str(e))
        return False
    else:
        flash("Confirmation email was send", category='success')
        return True


def validate_token(token):
    '''
    One hour TTL confirmationlinks
    TODO Need use env var for config it
    '''
    try:
        email = s.loads(token, salt='confirm', max_age=3600)
    except SignatureExpired:
        flash("Confirmation link expired", category='warning')
        return False
    except BadTimeSignature:
        flash("Confirmation link invalid", category='warning')
        return False
    else:
        flash("Confirmation link approved", category='success')
        return email
