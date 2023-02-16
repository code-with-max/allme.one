from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Pinterest
from app.models.networks import networks_data


@bp.route('/pinterest/<action>/', methods=('GET', 'POST'))
@login_required
def pinterest(action):
    if action == 'edit':
        if len(current_user.links[0].pinterest) > 0:
            pinterest = current_user.links[0].pinterest[0]
        else:
            pinterest = Pinterest(
                username='',
                )
            current_user.links[0].pinterest.append(pinterest)
            db.session.add(pinterest)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].pinterest) > 0:
            pinterest = current_user.links[0].pinterest[0]
            db.session.delete(pinterest)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        pinterest.username = username
        db.session.add(pinterest)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=pinterest,
        user=current_user,
        centered_view=True,
        network_data=networks_data['pinterest']
        )
