from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Github
# from app.models.networks import networks_data


@bp.route('/github/<action>/', methods=('GET', 'POST'))
@login_required
def github(action):
    if action == 'edit':
        if len(current_user.links[0].github) > 0:
            github = current_user.links[0].github[0]
        else:
            github = Github(
                username='',
                )
            current_user.links[0].github.append(github)
            db.session.add(github)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].github) > 0:
            github = current_user.links[0].github[0]
            db.session.delete(github)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        github.username = username
        db.session.add(github)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=github,
        user=current_user,
        )
