from flask_mail import Message
from itsdangerous import SignatureExpired
from smtplib import SMTPServerDisconnected
from app.extensions import mail
from app.auth import s  # FIXME I think need another variable name
from config import Config


def send_verification_email(email_adress):
    '''
    Sending email with verification link :)
    '''
    token = s.dumps(email_adress, salt='confirm')  # FIXME Must use env var
    msg = Message("Email confirmation",
                  sender="support@allme.one",
                  recipients=[email_adress])
    msg.html = "<b> testing of email confirmation </b>"
    print(Config.MAIL_SERVER)
    try:
        mail.send(msg)
    except SMTPServerDisconnected:
        return "SMTPServerDisconnected"
    except Exception as e:
        return e
    else:
        return "Email sent"
