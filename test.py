import requests
import json
import os
import yaml

def init():
    config_dir = os.path.dirname(__file__)
    rel_path = 'config.yml'
    abs_file_path = os.path.join(config_dir, rel_path)

    with open(abs_file_path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)


    print('------ config-------')
    configs = cfg[0]
    print(configs)
    print('------- common ---------------')
    common_setting = cfg[1]
    print(common_setting)
    print('-------- test -----------')
    tests = cfg[2]
    print(tests)
    print(type(tests))
    print('-----------  get tests  -----------')
    test_values = tests['tests']
    print(test_values)
    print('-----------  iterate tests  -----------')
    # iterate the test in tests yaml file
    for individual_test in test_values:
        # retrieves the individual test yamls in the tests block
        test = individual_test['test']
        # iterate the attributes of the test yaml
        for params in test:
            key = params.keys()[0]
            if key == 'name':
                print('---------------')
            #print(key, params[key])
            print(params[key])



            #url = 'https://{0}/services/search/duvet.do'.format(dns.rstrip())

    return ''


def get_requests_ocp_search():

    url = create_url()
#    headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web', 'Accept': 'application/json'}
#    r = requests.get(url, verify=False, headers=headers)
#    return r

resp = get_requests_ocp_search()

#status code

#pretty print
#parsed = json.dumps(resp.json(), indent=4)
#print parsed

