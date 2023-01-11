from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db


@bp.route('/email/<action>/', methods=('GET', 'POST'))
@login_required
def email(action):
    '''E-mail page edit'''
    if action == 'edit':
        email = current_user.links[0].email[0]
        if request.method == 'POST':
            adress = request.form['adress']
            description = request.form['description']

            email.adress = adress
            email.description = description

            db.session.add(email)
            db.session.commit()

            return redirect(url_for('main.home'))
        return render_template('links//home/edit/email.html',
                               email=email,
                               user=current_user,
                               )
