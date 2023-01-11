from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Cloudtips
# from app.models.networks import networks_data


@bp.route('/cloudtips/<action>/', methods=('GET', 'POST'))
@login_required
def cloudtips(action):
    if action == 'edit':
        if len(current_user.links[0].cloudtips) > 0:
            cloudtips = current_user.links[0].cloudtips[0]
        else:
            cloudtips = Cloudtips(
                username='',
                )
            current_user.links[0].cloudtips.append(cloudtips)
            db.session.add(cloudtips)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].cloudtips) > 0:
            cloudtips = current_user.links[0].cloudtips[0]
            db.session.delete(cloudtips)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        cloudtips.username = username
        db.session.add(cloudtips)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=cloudtips,
        user=current_user,
        )
