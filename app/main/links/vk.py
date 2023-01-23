from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Vkontakte
# from app.models.networks import networks_data


@bp.route('/vk/<action>/', methods=('GET', 'POST'))
@login_required
def vk(action):
    if not current_user.is_paying():
        return '<h3> You must pay </h3>'
    if action == 'edit':
        if len(current_user.links[0].vkontakte) > 0:
            vkontakte = current_user.links[0].vkontakte[0]
        else:
            vkontakte = Vkontakte(
                username='',
                )
            current_user.links[0].vkontakte.append(vkontakte)
            db.session.add(vkontakte)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].vkontakte) > 0:
            vkontakte = current_user.links[0].vkontakte[0]
            db.session.delete(vkontakte)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        vkontakte.username = username
        db.session.add(vkontakte)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=vkontakte,
        user=current_user,
        centered_view=True,
        )
