from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Instagram
# from app.models.networks import networks_data


@bp.route('/instagram/<action>/', methods=('GET', 'POST'))
@login_required
def instagram(action):
    if action == 'edit':
        if len(current_user.links[0].instagram) > 0:
            instagram = current_user.links[0].instagram[0]
        else:
            instagram = Instagram(
                username='You instagram username',
                )
            current_user.links[0].instagram.append(instagram)
            db.session.add(instagram)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].instagram) > 0:
            instagram = current_user.links[0].instagram[0]
            db.session.delete(instagram)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        instagram.username = username
        db.session.add(instagram)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/instagram.html',
        instagram=instagram,
        user=current_user,
        )
