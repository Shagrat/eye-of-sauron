import yaml
from flask import current_app


def get_sites_from_io():
    print(current_app.config.get('DATA_PATH'))
    with open(current_app.config.get('DATA_PATH'), 'a+') as stream:
        stream.seek(0)
        try:
            sites = list(yaml.load(stream))
        except TypeError:
            sites = []
    parsed = {}
    for site in sites:
        if not isinstance(site, dict):
            parsed[site] = {
                'url': site,
                'last_status': 'Unknown',
                'last_checked': None
            }
        else:
            parsed[site.get('url')] = {
                'url': site.get('url'),
                'last_status': site.get('status', 'Unknown'),
                'last_checked': None
            }
    return parsed


def update_sites_in_io(url, updated_url=False, delete=False):
    with open(current_app.config.get('DATA_PATH'), 'a+') as stream:
        stream.seek(0)
        try:
            sites = list(yaml.load(stream))
        except TypeError:
            sites = []
    parsed = {}
    for site in sites:
        if not isinstance(site, dict):
            parsed[site] = {
                'url': site,
                'last_status': 'Unknown',
                'last_checked': None
            }
        else:
            parsed[site.get('url')] = {
                'url': site.get('url'),
                'last_status': site.get('status', 'Unknown'),
                'last_checked': None
            }
    if not updated_url and not delete:
        parsed[url] = {
            'url': url,
            'last_status': 'Unknown',
            'last_checked': None
        }
    elif not delete:
        parsed.pop(url, None)
        parsed[updated_url] = {
            'url': updated_url,
            'last_status': 'Unknown',
            'last_checked': None
        }
    else:
        parsed.pop(url, None)
    with open(current_app.config.get('DATA_PATH'), 'w') as stream:
        yaml.dump([v for k, v in parsed.items()], stream)
    return parsed
