from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Twitter
# from app.models.networks import networks_data


@bp.route('/twitter/<action>/', methods=('GET', 'POST'))
@login_required
def twitter(action):
    if action == 'edit':
        if len(current_user.links[0].twitter) > 0:
            twitter = current_user.links[0].twitter[0]
        else:
            twitter = Twitter(
                username='',
                )
            current_user.links[0].twitter.append(twitter)
            db.session.add(twitter)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].twitter) > 0:
            twitter = current_user.links[0].twitter[0]
            db.session.delete(twitter)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        twitter.username = username
        db.session.add(twitter)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=twitter,
        user=current_user,
        )
