import requests
import json
import status_check
import os

def create_url():
    config_dir = os.path.dirname(__file__)
    print(config_dir)
    rel_path = 'config.txt'
    print(rel_path)
    abs_file_path = os.path.join(config_dir, rel_path)
    print(abs_file_path)

    with open(abs_file_path) as f:
        for dns in f:
            url = 'https://{0}/services/search/duvet.do'.format(dns.rstrip())

    return url

def get_requests_github():
    r = requests.get('https://api.github.com/events')
    return r

def get_requests_ocp_search():
    url = create_url()
    headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web',
               'Accept': 'application/json'}
    r = requests.get(url, verify=False, headers=headers)
    return r

resp = get_requests_ocp_search()

#status code
status_check.check_statuses(resp)

#pretty print
Eparsed = json.dumps(resp.json(), indent=4)
#print parsed

