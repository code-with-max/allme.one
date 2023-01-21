from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Telegram
# from app.models.networks import networks_data


@bp.route('/telegram/<action>/', methods=('GET', 'POST'))
@login_required
def telegram(action):
    if action == 'edit':
        if len(current_user.links[0].telegram) > 0:
            telegram = current_user.links[0].telegram[0]
        else:
            telegram = Telegram(
                username='',
                )
            current_user.links[0].telegram.append(telegram)
            db.session.add(telegram)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].telegram) > 0:
            telegram = current_user.links[0].telegram[0]
            db.session.delete(telegram)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        telegram.username = username
        db.session.add(telegram)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=telegram,
        user=current_user,
        centered_view=True,
        )
