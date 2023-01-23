from flask import render_template
from flask import redirect, url_for
from flask import request
from flask import jsonify
# from flask import flash
from flask_login import login_required, current_user
from app.api2 import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data
from app.main.collector import collect_links_data


@bp.route('/getlist/', methods=['GET', 'POST'])
# Get func from main blueprint :(
def short_list_of_links():

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.get_json()
            try:
                unique_link = json['card']
            except KeyError:
                return jsonify({'error': 'card key required'})                       
            user_list = Links.query.filter_by(unique_link=unique_link).first()
            if not user_list:
                return jsonify({'error': 'user card not found'})
            links_data, owner_is_paying = collect_links_data(user_list)
            return jsonify(links_data)
        else:
            return jsonify({'error': 'Content-Type not supported!'})
    elif request.method == 'GET':
        args = request.args
        unique_link = args.get('card')
        if not unique_link:
            return jsonify({'error': 'card key required'})
        user_list = Links.query.filter_by(unique_link=unique_link).first()
        if not user_list:
            return jsonify({'error': 'user card not found'})
        links_data, owner_is_paying = collect_links_data(user_list)
        return jsonify(links_data)
    # user_list = Links.query.filter_by(unique_link=unique_link).first()
