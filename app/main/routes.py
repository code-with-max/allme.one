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
    user_links = Links.query.filter_by(unique_link=unique_link).first_or_404()
    if user_links:
        return render_template("list_of_links.html",
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


@bp.route('/email/<action>/', methods=('GET', 'POST'))
@login_required
def email(action):
    '''E-mail page edit'''
    if action == 'edit':
        email = current_user.links[0].email[0]
        if request.method == 'POST':
            adress = request.form['adress']
            description = request.form['description']

            email.adress = adress
            email.description = description

            db.session.add(email)
            db.session.commit()

            return redirect(url_for('main.home'))
        return render_template('links//home/edit/email.html',
                               email=email,
                               user=current_user,
                               )


@bp.route('/about/<action>/', methods=('GET', 'POST'))
@login_required
def about(action):
    '''About page edit'''
    if action == 'edit':
        if len(current_user.links[0].about) > 0:
            about = current_user.links[0].about[0]
        else:
            from app.models.links import About
            about = About(username='', description='')
            current_user.links[0].about.append(about)
            db.session.add(about)
            db.session.commit()
            # about = current_user.links[0].about[0]
    elif action == 'delete':
        if len(current_user.links[0].about) > 0:
            about = current_user.links[0].about[0]
            db.session.delete(about)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form['user_name']
        description = request.form['description']

        about.username = name
        about.description = description

        db.session.add(about)
        db.session.commit()

        return redirect(url_for('main.home'))
    return render_template('links/home/edit/about.html',
                           about=about,
                           user=current_user,
                           )


def create_in_database(req):
    if req == 'facebook':
        from app.models.links import Facebook
        new_link = Facebook(username='', network_name=req)
        current_user.links[0].facebook.append(new_link)
        db.session.add(new_link)
        db.session.commit()

    elif req == 'instagram':
        from app.models.links import Instagram
        new_link = Instagram(username='', network_name=req)
        current_user.links[0].instagram.append(new_link)
        db.session.add(new_link)
        db.session.commit()

    elif req == 'vkontakte':
        from app.models.links import Vkontakte
        new_link = Vkontakte(username='', network_name=req)
        current_user.links[0].vkontakte.append(new_link)
        db.session.add(new_link)
        db.session.commit()
