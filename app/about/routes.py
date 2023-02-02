from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import jsonify
# from flask import flash
from flask_login import login_required, current_user
from app.about import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data
from app.main.collector import collect_links_data


# TODO Move "support@allme.one" to config ENV
@bp.route('/')
def about():
    return render_template('about/about.html',
                           centered_view=True,
                           )


@bp.route('/pp')
def pp():
    return render_template('about/privacy_policy.html')


@bp.route('/ts/')
def ts():
    return render_template('about/terms_of_service.html')
