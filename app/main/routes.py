from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Links


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
    user_links = {}
    grey_links = {}
    avaible_links = []
    postpaid_links = []
    user_pay = True if current_user.payment_state != 'white' else False

    flash(f'User payd status: {user_pay}', category='warning')

    if current_user.links[0].about:
        user_links['about'] = current_user.links[0].about[0]
    else:
        avaible_links.append('about')

    if current_user.links[0].email:
        user_links['email'] = current_user.links[0].email[0]
    else:
        avaible_links.append('email')

    if current_user.links[0].twitter:
        user_links['twitter'] = current_user.links[0].twitter[0]
    else:
        avaible_links.append('twitter')

    if current_user.links[0].facebook:
        user_links['facebook'] = current_user.links[0].facebook[0]
    else:
        avaible_links.append('facebook')

    if current_user.links[0].vkontakte:
        if user_pay:
            user_links['vkontakte'] = current_user.links[0].vkontakte[0]
        else:
            grey_links['vkontakte'] = current_user.links[0].vkontakte[0]
    else:
        if user_pay:
            avaible_links.append('vkontakte')
        else:
            postpaid_links.append('vkontakte')

    return render_template('home.html',
                           user=current_user,
                           ulinks=user_links,
                           glinks=grey_links,
                           alinks=avaible_links,
                           plinks=postpaid_links,
                           )


@bp.route('/email/<action>/', methods=('GET', 'POST'))
@login_required
def email(action):
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
        return render_template('links/email_edit.html',
                               email=email,
                               user=current_user,
                               )


@bp.route('/about/<action>/', methods=('GET', 'POST'))
@login_required
def about(action):
    if action == 'edit':
        if len(current_user.links[0].about) > 0:
            about = current_user.links[0].about[0]
        else:
            from app.models.links import About
            about = About(name='', description='')
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

        about.name = name
        about.description = description

        db.session.add(about)
        db.session.commit()

        return redirect(url_for('main.home'))
    return render_template('links/about_edit.html',
                           about=about,
                           user=current_user,
                           )
