from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.api2 import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data
from app.main.collector import collect_links_data


@bp.route('/<unique_link>/')
# Get func from main blueprint :(
def short_list_of_links(unique_link):
    links_data = collect_links_data(unique_link)
    return render_template('api2/api2.html',
                           links_data=links_data,
                           )
