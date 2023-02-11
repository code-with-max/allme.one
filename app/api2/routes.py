from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import jsonify
# from flask import flash
from flask_login import login_required, current_user
from app.api2 import bp
from app.extensions import db
from app.models import User, Apikey
from app.models.links import Links
from app.models.networks import networks_data
from app.main.collector import collect_links_data


@bp.route('/getlist/', methods=['GET', 'POST'])
# OperationalError
# Get func from main blueprint :(
def api_list_of_links():
    # Validate request (POST and GET)
    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            try:
                api_key = json['key']
            except KeyError:
                return jsonify({'error': 'API-key required'})
            try:
                unique_link = json['card']
            except KeyError:
                return jsonify({'error': 'Card link required'})
        else:
            return jsonify({'error': 'Content-Type not supported!'})
    elif request.method == 'GET':
        api_key = request.args.get('key')
        if not api_key:
            return jsonify({'error': 'API-key required'})
        unique_link = request.args.get('card')
        if not unique_link:
            return jsonify({'error': 'Card link required'})
    # Validate user
    user_api = db.one_or_404(db.select(Apikey).filter_by(key=api_key))
    print(user_api)
    if not user_api.user.is_paying():
        user_api.count += 1
        if user_api.count > 99:  # TODO move request limit to app config
            return jsonify({'error': 'API key request limit has been reached'})
    print(user_api.count)
    # Validate list of links
    list = db.one_or_404(db.select(Links).filter_by(unique_link=unique_link))
    # Get links data
    links_data = collect_links_data(list)
    # And return :)
    db.session.commit()
    return jsonify(links_data)


@bp.route('/keys/')
@login_required
def keys():
    api_keys = current_user.api_keys
    can_create = False
    # TODO move limits to app config
    if current_user.is_paying() and len(api_keys) < 9:
        can_create = True
    elif len(api_keys) < 2:
        can_create = True
    return render_template("api2/apikeys.html",
                           keys=current_user.api_keys,
                           can_create=can_create,
                           user_is_paying=current_user.is_paying(),
                           )


@bp.route('/deletekey/<key>')
@login_required
def delete_key(key):
    for api_key in current_user.api_keys:
        if key == api_key.key:
            print(api_key)
            # TODO OperationalError
            db.session.delete(api_key)
            db.session.commit()
    return redirect(url_for('api2.keys'))


@bp.route('addkey')
@login_required
def add_key():
    new_key = Apikey()
    db.session.add(new_key)
    current_user.api_keys.append(new_key)
    db.session.commit()
    return redirect(url_for('api2.keys'))
