from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Steamdeveloper
from app.models.networks import networks_data


@bp.route('/steamdeveloper/<action>/', methods=('GET', 'POST'))
@login_required
def steamdeveloper(action):
    if action == 'edit':
        if len(current_user.links[0].steamdeveloper) > 0:
            steamdeveloper = current_user.links[0].steamdeveloper[0]
        else:
            steamdeveloper = Steamdeveloper(
                username='',
                )
            current_user.links[0].steamdeveloper.append(steamdeveloper)
            db.session.add(steamdeveloper)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].steamdeveloper) > 0:
            steamdeveloper = current_user.links[0].steamdeveloper[0]
            db.session.delete(steamdeveloper)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        steamdeveloper.username = username
        db.session.add(steamdeveloper)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=steamdeveloper,
        user=current_user,
        centered_view=True,
        network_data=networks_data['steamdeveloper']
        )
