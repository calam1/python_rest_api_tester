import os
import yaml
import collections
from rest_get import RestTestGet

def _open_and_load_yaml_file():
    config_dir = os.path.dirname(__file__)
    rel_path = 'config.yml'
    abs_file_path = os.path.join(config_dir, rel_path)

    with open(abs_file_path, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    return cfg

def _get_host_name(cfg):
    configs = cfg[0]
    config_list = configs['config']
    hostname = ''
    for c in config_list:
        hostname = c['hostname']

    return hostname


def _get_headers(cfg):
    common_settings = cfg[1]
    headers = ''
    for common_setting in common_settings:
        cs = common_settings[common_setting]
        for c in cs:
            headers = c['headers']

    return headers

def _get_test_attributes(cfg):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'url', 'method'])

    tests = cfg[2]
    test_values = tests['tests']
    test_attributes = list()

    # iterate the test in tests yaml file
    for individual_test in test_values:
        # retrieves the individual test yamls in the tests block
        test = individual_test['test']
        # iterate the attributes of the test yaml
        name = ''
        url = ''
        method = ''

        for params in test:
            key = params.keys()[0]
            if key == 'name':
                name = params[key]

            if key == 'url':
                url = params[key]

            if key == 'method':
                method = params[key]

        test_attribute = TestAttributes(name, url, method)
        test_attributes.append(test_attribute)

    return test_attributes

def _generate_url(hostname, attributes):
    url = 'https://{0}{1}'
    url = url.format(hostname, attributes.url)

    return url

def init():
    _cfg = _open_and_load_yaml_file()

    _hostname = _get_host_name(_cfg)
    _headers = _get_headers(_cfg)
    _attributes = _get_test_attributes(_cfg)

    for a in _attributes:
        _restful_url = _generate_url(_hostname, a)
        print(_restful_url)
        rest_get = RestTestGet(_restful_url, _headers)
        response = rest_get.get_response()
        print(response)

init()
