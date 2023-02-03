from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Flickr
from app.models.networks import networks_data


@bp.route('/flickr/<action>/', methods=('GET', 'POST'))
@login_required
def flickr(action):
    if action == 'edit':
        if len(current_user.links[0].flickr) > 0:
            flickr = current_user.links[0].flickr[0]
        else:
            flickr = Flickr(
                username='',
                )
            current_user.links[0].flickr.append(flickr)
            db.session.add(flickr)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].flickr) > 0:
            flickr = current_user.links[0].flickr[0]
            db.session.delete(flickr)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        flickr.username = username
        db.session.add(flickr)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=flickr,
        user=current_user,
        centered_view=True,
        network_data=networks_data['flickr']
        )
