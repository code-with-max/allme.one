from flask import render_template
from flask import redirect, url_for
from flask import request
from flask_login import login_required, current_user
from app.main import bp
from app.extensions import db
from app.models.links import About


@bp.route('/about/<action>/', methods=('GET', 'POST'))
@login_required
def about(action):
    '''About page edit'''
    if action == 'edit':
        if len(current_user.links[0].about) > 0:
            about = current_user.links[0].about[0]
        else:
            about = About(username='', description='')
            current_user.links[0].about.append(about)
            db.session.add(about)
            db.session.commit()
            # about = current_user.links[0].about[0]
    elif action == 'delete':
        if len(current_user.links[0].about) > 0:
            about = current_user.links[0].about[0]
            db.session.delete(about)
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            # Need redirect to 404 page!
            return redirect(url_for('main.home'))

    if request.method == 'POST':
        name = request.form['user_name']
        description = request.form['description']

        name = name.strip()
        desc = description.strip()
        about.username = f'{name:.32}' if len(name) > 32 else name
        about.description = f'{desc:.255}' if len(desc) > 255 else desc

        db.session.add(about)
        db.session.commit()

        return redirect(url_for('main.home'))
    return render_template('links/home/edit/about.html',
                           about=about,
                           user=current_user,
                           centered_view=True,
                           )
