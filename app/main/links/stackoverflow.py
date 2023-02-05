from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Stackoverflow
from app.models.networks import networks_data


@bp.route('/stackoverflow/<action>/', methods=('GET', 'POST'))
@login_required
def stackoverflow(action):
    if action == 'edit':
        if len(current_user.links[0].stackoverflow) > 0:
            stackoverflow = current_user.links[0].stackoverflow[0]
        else:
            stackoverflow = Stackoverflow(
                username='',
                )
            current_user.links[0].stackoverflow.append(stackoverflow)
            db.session.add(stackoverflow)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].stackoverflow) > 0:
            stackoverflow = current_user.links[0].stackoverflow[0]
            db.session.delete(stackoverflow)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        stackoverflow.username = username
        db.session.add(stackoverflow)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=stackoverflow,
        user=current_user,
        centered_view=True,
        network_data=networks_data['stackoverflow']
        )
