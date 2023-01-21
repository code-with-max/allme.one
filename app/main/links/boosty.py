from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Boosty
# from app.models.networks import networks_data


@bp.route('/boosty/<action>/', methods=('GET', 'POST'))
@login_required
def boosty(action):
    if action == 'edit':
        if len(current_user.links[0].boosty) > 0:
            boosty = current_user.links[0].boosty[0]
        else:
            boosty = Boosty(
                username='',
                )
            current_user.links[0].boosty.append(boosty)
            db.session.add(boosty)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].boosty) > 0:
            boosty = current_user.links[0].boosty[0]
            db.session.delete(boosty)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        boosty.username = username
        db.session.add(boosty)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=boosty,
        user=current_user,
        centered_view=True,
        )
