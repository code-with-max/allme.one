import os
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from paymentwall import Paymentwall, Product, Widget, Pingback
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
        't_00000001',  # uid
        'pw_1',  # widget
        [],  # [product], now empty for widgets API
        {
            'email': 'admin@deadend.xyz',
            'history[registration_date]': 'registered_date_of_user',
            'ps': 'all',  # Replace it with specific payment system short code for single payment methods
            'evaluation': 1,  # FIXME For test env only !!!
            'additional_param': 'param_value',
            'user_pay_code': '33195',
            'USER_ID': 't_000000001',
        }
    )
    # print(widget.get_url())
    payurl = widget.get_url()

    return render_template('paywall/make_payment.html',
                           payurl=payurl,
                           centered_view=True,
                           )


@bp.route('/pingback/', methods=['GET'])
def pingback():
    Paymentwall.set_api_type(Paymentwall.API_GOODS)
    Paymentwall.set_app_key(os.environ.get('PAYWALL_PROJECT_KEY'))
    Paymentwall.set_secret_key(os.environ.get('PAYWALL_SECRET_KEY'))

    # if request.method == 'GET':
    #     print(request.args.items())
    #     print(request.remote_addr)

    pingback = Pingback({x:y for x, y in request.args.items()}, '174.36.96.66')
    # print(dir(pingback))

    if pingback.validate():
        product_id = pingback.get_product().get_id()
        print(product_id)
        if pingback.is_deliverable():
            print(product_id)
            pass
        elif pingback.is_cancelable():
            # withdraw the product
            pass

        # print('OK')  # Paymentwall expects response to be OK, otherwise the pingback will be resent

    # else:
        # print(pingback.get_error_summary())

    return 'OK', 200
