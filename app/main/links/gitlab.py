from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Gitlab
from app.models.networks import networks_data


@bp.route('/gitlab/<action>/', methods=('GET', 'POST'))
@login_required
def gitlab(action):
    if action == 'edit':
        if len(current_user.links[0].gitlab) > 0:
            gitlab = current_user.links[0].gitlab[0]
        else:
            gitlab = Gitlab(
                username='',
                )
            current_user.links[0].gitlab.append(gitlab)
            db.session.add(gitlab)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].gitlab) > 0:
            gitlab = current_user.links[0].gitlab[0]
            db.session.delete(gitlab)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        gitlab.username = username
        db.session.add(gitlab)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=gitlab,
        user=current_user,
        centered_view=True,
        network_data=networks_data['gitlab']
        )
