from app.main import bp
from app.extensions import db
from app.models.links import Links
from app.models.networks import networks_data


def collect_links_data(unique_link):
    '''
    Generate lists of user links by unique identifer \n
    Avaible groups for filtering: \n
    sm - social media,
    ms - messengers,
    dw - donations world,
    dr - donation Russia,
    em - emails,
    pe - personal links,
    in - info (About etc..)
    else: nc - no category list
    '''
    user_list = Links.query.filter_by(unique_link=unique_link).first_or_404()
    if user_list:
        response = {}
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
                    }
            link_key = {
                key: link_data
            }
            if group not in response.keys():
                response[group] = link_key
            else:
                response[group].update(link_key)
        return response
    else:
        return False
