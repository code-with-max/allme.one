from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Playmarket
# from app.models.networks import networks_data


@bp.route('/playmarket/<action>/', methods=('GET', 'POST'))
@login_required
def playmarket(action):
    if action == 'edit':
        if len(current_user.links[0].playmarket) > 0:
            playmarket = current_user.links[0].playmarket[0]
        else:
            playmarket = Playmarket(
                username='',
                )
            current_user.links[0].playmarket.append(playmarket)
            db.session.add(playmarket)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].playmarket) > 0:
            playmarket = current_user.links[0].playmarket[0]
            db.session.delete(playmarket)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        playmarket.username = username
        db.session.add(playmarket)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=playmarket,
        user=current_user,
        centered_view=True,
        )
