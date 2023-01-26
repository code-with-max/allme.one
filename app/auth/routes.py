import string
import random
from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import bp
from app.extensions import db
from app.models.user import User
from app.models.links import Links, Email


def hash_password(password):
    ''' Generate password hash using sha256'''
    return generate_password_hash(password, method='sha256')


def get_random_link(length):
    ''' Generate unique random link for new user '''
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    while result_str == Links.query.filter_by(unique_link=result_str).first():
        result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@bp.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You a logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('main.home'))
            else:
                flash("Wrong password", category='warning')
        else:
            flash("Email does not exist", category='warning')

    return render_template('auth/login.html',
                        #    user=current_user,
                           centered_view=True,
                           )


@bp.route('/logout/')
@login_required
def logout():
    unique_link = current_user.get_list().unique_link
    logout_user()
    # Need delete this flash message
    # flash(f'Is_authenticated: {current_user.is_authenticated}')
    return redirect(url_for(
                        "main.short_list_of_links",
                        unique_link=unique_link
                        )
                    )


@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        request_email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exist = User.query.filter_by(email=request_email).first()
        if email_exist:
            flash("E-mail already used", category='warning')
        elif len(password1) < 6:
            flash("Password is to short", category='warning')
        elif password1 != password2:
            flash("Passwords dont match", category='warning')
        else:
            user_email = Email(username=request_email)
            user_links = Links(email=[user_email],
                               unique_link=get_random_link(9),
                               )
            db.session.add(user_email, user_links)
            new_user = User(email=request_email,
                            password=hash_password(password1),
                            links=[user_links],
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created", category='success')
            return redirect(url_for('main.home'))

    return render_template(
                    'auth/signup.html',
                    # user=current_user,
                    centered_view=True,
                    )


@bp.route('/newpass/', methods=['GET', 'POST'])
@login_required
def newpass():
    if request.method == 'POST':
        password0 = request.form.get('password0')  # Old password
        password1 = request.form.get('password1')  # New password
        password2 = request.form.get('password2')  # Retyped new password

        if not check_password_hash(current_user.password, password0):
            flash("Current password incorrect", category='warning')
        elif password1 != password2:
            flash("New passwords mismatch", category='warning')
        elif len(password1) < 6:
            flash("The new password is too short", category='warning')
        elif check_password_hash(current_user.password, password1):
            flash("The new password matches the old", category='warning')
        else:
            current_user.password = hash_password(password1)
            db.session.add(current_user)
            db.session.commit()
            flash("Password changed", category='success')
            return redirect(url_for('main.settings'))

    return render_template(
                    'auth/newpass.html',
                    # user=current_user,  # TODO parametr not used
                    centered_view=True,
                    )
