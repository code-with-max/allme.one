import os
from flask_mail import Message
from smtplib import SMTPServerDisconnected
from flask import render_template, url_for
from app.extensions import mail


def send_confirmation_email(email_adress: str, user_lang: str) -> bool:
    '''
    Sending change payment status confirmation email
    '''

    if user_lang == 'RU':
        msg_subject = 'Ваш статус пользователя изменен'
        msg_body_template = 'mail/paywall/email_confirmation_RU.html'
    else:
        msg_subject = 'You status changed to PRO'
        msg_body_template = 'mail/paywall/email_confirmation_EN.html'

    site_url = url_for('main.index', _external=True)
    # TODO Move into config or env
    github_url = 'https://github.com/trash-max/allme.one'
    boosty_url = 'https://boosty.to/codewithmax'
    cloudtips_url = 'https://pay.cloudtips.ru/p/5acab2cd'
    patreon_url = 'https://www.patreon.com/codewithmax'
    bmc_url = 'https://www.buymeacoffee.com/maxtrash'
    msg = Message(msg_subject,
                  sender="support@allme.one",  # FIXME Must use env var
                  recipients=[email_adress])
    msg.html = render_template(msg_body_template,
                               site_url=site_url,
                               github_url=github_url,
                               boosty_url=boosty_url,
                               cloudtips_url=cloudtips_url,
                               patreon_url=patreon_url,
                               bmc_url=bmc_url,
                               )
    try:
        mail.send(msg)
    except SMTPServerDisconnected:
        return False
    except Exception as e:
        # TODO smtp server errors need to be handled
        # https://docs.python.org/3/library/smtplib.html
        if os.environ.get('FLASK_DEBUG'):
            print(f'Error with confirm payment e-mail: {e}')
        return False
    else:
        return True
