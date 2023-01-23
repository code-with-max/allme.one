# from app.main import bp
# from app.extensions import db
# from app.models.links import Links
from app.models.networks import networks_data


def collect_links_data(list):
    '''
    Return tuple of [user links data, payment status],
    require SQLAlchemy list object as positional argument \n
    Usage example: \n
    list_data, payment_status = collect_links_data(list_object)
    '''
    user_list = list
    response = {}
    user_is_paying = user_list.user.is_paying()
    user_links, free_links = user_list.get_links()
    for link in user_links:
        full_url = networks_data[link.network_name]['url'] + link.username
        group = networks_data[link.network_name]['group']
        key = str(link.network_name)
        link_data = {
                'full_url': full_url,
                'username': link.username,
                'title': link.get_title(),
                'about': link.about,
                'description': link.description,
                }
        link_key = {
            key: link_data
        }
        if group not in response.keys():
            response[group] = link_key
        else:
            response[group].update(link_key)
    return response, user_is_paying
