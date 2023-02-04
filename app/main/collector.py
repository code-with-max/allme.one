from flask import url_for
from app.models.networks import networks_data


def collect_links_data(user_list: object) -> dict:
    '''
    Return user links data as dictionary,
    require SQLAlchemy list object as positional argument \n
    Usage example: \n
    user_list = collect_links_data(list_object)
    '''
    response = {}
    user_is_paying = user_list.user.is_paying()  # TODO Need pay check
    user_links, free_links = user_list.get_links()
    for link in user_links:
        full_url = networks_data[link.network_name]['url'] + link.username
        repr_name = networks_data[link.network_name]['repr_name']
        icon = networks_data[link.network_name]['icon_name']
        group = networks_data[link.network_name]['group']
        key = str(link.network_name)
        link_data = {
                'full_url': full_url,
                'username': link.username,
                'about': link.about,
                'description': link.description,
                'icon': icon,
                'repr_name': repr_name,
                }
        link_key = {
            key: link_data
        }
        if group not in response.keys():
            response[group] = link_key
        else:
            response[group].update(link_key)
    return response


def collect_share_data(unique_link: str) -> dict:
    response = {}
    for key, data in networks_data.items():
        if data['share_url']:
            user_url = url_for('main.short_list_of_links',
                               unique_link=unique_link,
                               _external=True,
                               )
            share_data = {
                'share_url': f"{data['share_url']}{user_url}",
                'icon': data['icon_name'],
                'repr_name': data['repr_name'],
                }
            response[key] = share_data
    return response
