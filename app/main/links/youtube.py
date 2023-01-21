from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Youtube
# from app.models.networks import networks_data


@bp.route('/youtube/<action>/', methods=('GET', 'POST'))
@login_required
def youtube(action):
    if action == 'edit':
        if len(current_user.links[0].youtube) > 0:
            youtube = current_user.links[0].youtube[0]
        else:
            youtube = Youtube(
                username='',
                )
            current_user.links[0].youtube.append(youtube)
            db.session.add(youtube)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].youtube) > 0:
            youtube = current_user.links[0].youtube[0]
            db.session.delete(youtube)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        youtube.username = username
        db.session.add(youtube)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=youtube,
        user=current_user,
        centered_view=True,
        )
