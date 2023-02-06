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

    product = Product(
        'product301',  # ag_external_id
        9.99,
        'USD',
        'Gold Membership',
        Product.TYPE_FIXED
    )

    widget = Widget(
        'user40012',  # uid
        'p1_1',  # widget
        [product],
        {
            'email': 'user@hostname.com',
            'history[registration_date]': 'registered_date_of_user',
            'ps': 'all',  # Replace it with specific payment system short code for single payment methods
            'additional_param_name': 'additional_param_value'
        }
    )
    print(widget.get_url())
    payurl = widget.get_url()

    return render_template('paywall/make_payment.html', payurl=payurl)
    # return url_for(payurl, _external=True)
