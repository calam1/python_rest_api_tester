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
    config_list = configs.get('config')
    hostname = ''
    for c in config_list:
        hostname = c.get('hostname')

    return hostname

def get_headers(cfg):
    common_settings = cfg[1]
    headers = ''
    for common_setting in common_settings:
        cs = common_settings[common_setting]
        for c in cs:
            headers = c.get('headers')

    return headers

def get_test_attributes(cfg):
    tests = cfg[2]
    test_values = tests.get('tests')
    test_attributes = list()

    # iterate the test in tests yaml file
    for individual_test in test_values:
        # retrieves the individual test yamls in the tests block
        test = individual_test.get('test')
        test_attribute = _build_test_attributes(test)
        test_attributes.append(test_attribute)

    return test_attributes

def _build_test_attributes(test):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'prep_states', 'url', 'method', 'payload', 'comparisons'])

    prep_states = list()
    name = None
    url = None
    method = None
    payload = None
    comparisons = None

    for params in test:
        if (filter(lambda x: x == 'name', params)):
            name = params.values()[0]

        if (filter(lambda x: x == 'prep_state', params)):
            prep_state = params.values()[0]
            #TODO will probably need to loop through this but for now it works
            test_attribute = _build_test_attributes(prep_state)
            prep_states.append(test_attribute)

        if len(filter(lambda x: x == 'url', params)):
            url = params.values()[0]

        if len(filter(lambda x: x == 'method', params)):
            method = params.values()[0]

        if len(filter(lambda x: x == 'payload', params)):
            payload = params.values()[0]

        if len(filter(lambda x: x == 'validations', params)):
            _validations = params.values()[0]
            comparisons = _get_comparisons(_validations)

    test_attribute = TestAttributes(name, prep_states, url, method, payload, comparisons)

    return test_attribute

def _get_comparisons(validations):
    comparisons = list()
    for comparison in validations:
        comparisons.append(comparison)

    return comparisons


def generate_url(hostname, attributes):
    url = 'https://{0}{1}'
    url = url.format(hostname, attributes.url)

    return url
