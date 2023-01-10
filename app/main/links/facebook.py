from flask import render_template
from flask import redirect, url_for
from flask import request
# from flask import flash
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import Facebook
# from app.models.networks import networks_data


@bp.route('/facebook/<action>/', methods=('GET', 'POST'))
@login_required
def facebook(action):
    if action == 'edit':
        if len(current_user.links[0].facebook) > 0:
            facebook = current_user.links[0].facebook[0]
        else:
            facebook = Facebook(
                username='You facebook username',
                )
            current_user.links[0].facebook.append(facebook)
            db.session.add(facebook)
            db.session.commit()

    elif action == 'delete':
        if len(current_user.links[0].facebook) > 0:
            facebook = current_user.links[0].facebook[0]
            db.session.delete(facebook)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        username = request.form['username']
        facebook.username = username
        db.session.add(facebook)
        db.session.commit()
        return redirect(url_for('main.home'))

    return render_template(
        'links/home/edit/facebook.html',
        facebook=facebook,
        user=current_user,
        )
