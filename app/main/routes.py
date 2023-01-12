from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    return render_template("index.html", user=current_user)


@bp.route('/<unique_link>/')
def list_of_links(unique_link):
    user_list = Links.query.filter_by(unique_link=unique_link).first_or_404()
    if user_list:
        user_links, free_links = user_list.get_links()
        return render_template("links/cards/short.html",
                               user=current_user,
                               links=user_links,
                               )
    else:
        # Need redirect to 404 page!
        return '<h1> oops... somethin wrong </h1>'


@bp.route('/home/')
@login_required
def home():
    ''' Draw control panel for logged user '''
    used_links, free_links = current_user.links[0].get_links()
    # I think need else more list of paid links...
    return render_template('home.html',
                           user=current_user,
                           used_links=used_links,
                           free_links=free_links,
                           networks=networks_data,
                           )
