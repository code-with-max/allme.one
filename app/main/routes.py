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
    return render_template("index.html", centered_view=True)


@bp.route('/<unique_link>/')
def short_list_of_links(unique_link):
    user_list = Links.query.filter_by(unique_link=unique_link).first_or_404()
    if user_list:
        data = {}
        user_links, free_links = user_list.get_links()
        for link in user_links:
            full_url = networks_data[link.network_name]['url'] + link.username
            data[str(link.network_name)] = {
                    'full_url': full_url,
                    'username': link.username,
                    'title': link.get_title(),
                    }
        print(data)
        return render_template("links/cards/short.html",
                               networks_data=networks_data,
                               links_data=data,
                               user_paiyng=user_list.user.is_paying(),
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
