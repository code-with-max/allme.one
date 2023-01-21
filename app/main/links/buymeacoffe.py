from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Buymeacoffe
# from app.models.networks import networks_data


@bp.route('/buymeacoffe/<action>/', methods=('GET', 'POST'))
@login_required
def buymeacoffe(action):
    if action == 'edit':
        if len(current_user.links[0].buymeacoffe) > 0:
            buymeacoffe = current_user.links[0].buymeacoffe[0]
        else:
            buymeacoffe = Buymeacoffe(
                username='',
                )
            current_user.links[0].buymeacoffe.append(buymeacoffe)
            db.session.add(buymeacoffe)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].buymeacoffe) > 0:
            buymeacoffe = current_user.links[0].buymeacoffe[0]
            db.session.delete(buymeacoffe)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        buymeacoffe.username = username
        db.session.add(buymeacoffe)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/common_edit.html',
        social_media=buymeacoffe,
        user=current_user,
        centered_view=True,
        )
