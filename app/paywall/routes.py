import os
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from paymentwall import Paymentwall, Product, Widget
from app.paywall import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data
from app.models.gravatar import Gravatar
from app.main.collector import collect_links_data, collect_share_data


@bp.route('/')
def make_payment():
    Paymentwall.set_api_type(Paymentwall.API_GOODS)
    Paymentwall.set_app_key(os.environ.get('PAYWALL_PROJECT_KEY'))
    Paymentwall.set_secret_key(os.environ.get('PAYWALL_SECRET_KEY'))

    #  This part will using with self building widgets
    #  https://docs.paymentwall.com/integration/checkout/onetime
    #  https://docs.paymentwall.com/integration/checkout/subscription
    product = Product(
        'test_id_00',  # ag_external_id
        9.99,
        'USD',
        'PRO version for one year',
        Product.TYPE_FIXED
    )

    widget = Widget(
        't_user40013',  # uid
        'pw_1',  # widget
        [],  # [product], now empty for widgets API
        {
            'email': 'admin@deadend.xyz',
            'history[registration_date]': 'registered_date_of_user',
            'ps': 'all',  # Replace it with specific payment system short code for single payment methods
            'evaluation': 1,  # FIXME For test env only !!!
            'additional_param': 'param_value',
            'user_pay_code': '33195'
        }
    )
    # print(widget.get_url())
    payurl = widget.get_url()

    return render_template('paywall/make_payment.html',
                           payurl=payurl,
                           centered_view=True,
                           )


@bp.route('/pingback/')
def pingback():
    return 'OK', 200
