import os
import yaml
import collections

def open_and_load_yaml_file():
    config_dir = os.path.dirname(__file__)
    rel_path = 'config.yml'
    abs_file_path = os.path.join(config_dir, rel_path)

    with open(abs_file_path, 'r') as _ymlfile:
        cfg = yaml.load(_ymlfile)

    return cfg

def get_host_name(cfg):
    configs = cfg[0]
    config_list = configs['config']
    hostname = ''
    for c in config_list:
        hostname = c['hostname']

    return hostname

def get_headers(cfg):
    common_settings = cfg[1]
    headers = ''
    for common_setting in common_settings:
        cs = common_settings[common_setting]
        for c in cs:
            headers = c['headers']

    return headers

def get_test_attributes(cfg):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'url', 'method', 'comparisons'])

    tests = cfg[2]
    test_values = tests['tests']
    test_attributes = list()

    # iterate the test in tests yaml file
    for individual_test in test_values:
        # retrieves the individual test yamls in the tests block
        test = individual_test['test']
        # iterate the attributes of the test yaml
        name = None
        url = None
        method = None
        comparisons = None

        for params in test:
            if len(filter(lambda x: x == 'name', params)) != 0:
                name = params.values()[0]

            if len(filter(lambda x: x == 'url', params)) != 0:
                url = params.values()[0]

            if len(filter(lambda x: x == 'method', params)) != 0:
                method = params.values()[0]

            if len(filter(lambda x: x == 'validations', params)) != 0:
                _validations = params.values()[0]
                comparisons = _get_comparisons(_validations)

        test_attribute = TestAttributes(name, url, method, comparisons)
        test_attributes.append(test_attribute)

    return test_attributes

def _get_comparisons(validations):
    comparisons = list()
    for comparison in validations:
        comparisons.append(comparison)

    return comparisons

def generate_url(hostname, attributes):
    url = 'https://{0}{1}'
    url = url.format(hostname, attributes.url)

    return url
