import os
import uuid
from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from paymentwall import Paymentwall, Product, Widget, Pingback
from app.paywall import bp
from app.paywall.utility import send_confirmation_email
from app.extensions import db
from app.models.links import Links
from app.models.user import User
from app.models.networks import networks_data
from app.models.gravatar import Gravatar
from app.main.collector import collect_links_data, collect_share_data
from app.auth import confirm_required


# FIXME Think I must using app.config
pingback_endpoint = os.environ.get('PAYWALL_PINGBACK')


@bp.route('/')
@login_required
# @confirm_required  # FIXME decorator raise wergzeug errors :()
def make_payment():
    if not current_user.email_confirmed:
        return redirect(url_for("auth.email_not_confirmed"))

    # FIXME Think I must using app.config
    Paymentwall.set_api_type(Paymentwall.API_GOODS)
    Paymentwall.set_app_key(os.environ.get('PAYWALL_PROJECT_KEY'))
    Paymentwall.set_secret_key(os.environ.get('PAYWALL_SECRET_KEY'))

    # FIX for OLD users.
    # TODO: Need make lambda for fix it
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr).split(',')[0]
    if current_user.update_geo_data(ip=ip_addr):
        db.session.commit()
    if not current_user.payment_UUID:
        new_UUID = uuid.uuid4()
        current_user.payment_UUID = new_UUID
        db.session.add(current_user)
        db.session.commit()

    uid = current_user.payment_UUID
    email = current_user.email

    #  This part will using with self building widgets
    #  https://docs.paymentwall.com/integration/checkout/onetime
    #  https://docs.paymentwall.com/integration/checkout/subscription
    product = Product(
                'product301',               # id of the product in your system 
                9.99,                       # price
                'USD',                      # currency code
                'Gold Membership',          # product name
                Product.TYPE_SUBSCRIPTION,  # this is a time-based product
                1,                          # duration is 1
                Product.PERIOD_TYPE_WEEK,   # week
                True                        # recurring
                )

    widget = Widget(
        uid,  # uid
        'pw_1',  # widget
        [],  # [product], now empty for widgets API
        {
            'email': email,
            'ps': 'all',  # Replace it with specific payment system short code for single payment methods
            'evaluation': 1,  # FIXME For test env only !!!
            'success_url': url_for('paywall.success', _external=True)
        }
    )
    # print(widget.get_url())
    payurl = widget.get_url()

    return render_template('paywall/make_payment.html',
                           payurl=payurl,
                           centered_view=True,
                           user_lang=current_user.countrycode
                           )


@bp.route(f'/{pingback_endpoint}/', methods=['GET'])
def pingback():
    # FIXME Think I must using app.config
    Paymentwall.set_api_type(Paymentwall.API_GOODS)
    Paymentwall.set_app_key(os.environ.get('PAYWALL_PROJECT_KEY'))
    Paymentwall.set_secret_key(os.environ.get('PAYWALL_SECRET_KEY'))

    if os.environ.get('FLASK_DEBUG'):
        # Pingback IP must be in 'white list' from paymentwall API
        # https://github.com/paymentwall/paymentwall-python
        r_addr = '174.36.96.66'
    else:
        r_addr = request.remote_addr

    pingback = Pingback({x:y for x, y in request.args.items()}, r_addr)

    if pingback.validate():
        product_id = pingback.get_product().get_id()
        uuid = pingback.get_user_id()
        user = User.query.filter_by(payment_UUID=uuid).first()

        if os.environ.get('FLASK_DEBUG'):
            print(f'Product: {product_id}')
            print(user)

        if user:
            if pingback.is_deliverable():
                if user.update_payment_status(product_id):
                    # db.session.add(user)
                    db.session.commit()
                    send_confirmation_email(user.email, user.countrycode)
            elif pingback.is_cancelable():
                # withdraw the product
                pass
        return 'OK', 200  # Paymentwall expects response to be OK, otherwise the pingback will be resent

    else:
        if os.environ.get('FLASK_DEBUG'):
            print(pingback.get_error_summary())
            # TODO implement mail notify about errors

    return 'Success', 200


@bp.route('/success/')
def success():
    flash("Payment accepted.)", category='success')
    return redirect(url_for('main.home'))
