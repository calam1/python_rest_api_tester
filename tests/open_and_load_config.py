import os
import yaml
import collections

def open_and_load_yaml_file():
    _config_dir = os.path.dirname(__file__)
    _rel_path = 'config.yml'
    _abs_file_path = os.path.join(_config_dir, _rel_path)

    with open(_abs_file_path, 'r') as _ymlfile:
        _cfg = yaml.load(_ymlfile)

    return _cfg

def get_host_name(cfg):
    _configs = cfg[0]
    _config_list = _configs['config']
    _hostname = ''
    for c in _config_list:
        _hostname = c['hostname']

    return _hostname

def get_headers(cfg):
    _common_settings = cfg[1]
    _headers = ''
    for common_setting in _common_settings:
        cs = _common_settings[common_setting]
        for c in cs:
            _headers = c['headers']

    return _headers

def get_test_attributes(cfg):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'url', 'method', 'comparisons'])

    _tests = cfg[2]
    _test_values = _tests['tests']
    _test_attributes = list()

    # iterate the test in tests yaml file
    for individual_test in _test_values:
        # retrieves the individual test yamls in the tests block
        _test = individual_test['test']
        # iterate the attributes of the test yaml
        _name = None
        _url = None
        _method = None
        _comparisons = None

        # maybe use filter to pull out keys and data
        for params in _test:
            key = params.keys()[0]
            if key == 'name':
                _name = params[key]

            if key == 'url':
                _url = params[key]

            if key == 'method':
                _method = params[key]

            if key == 'validations':
                _validations = params[key]
                _comparisons = _get_comparisons(_validations)

        _test_attribute = TestAttributes(_name, _url, _method, _comparisons)
        _test_attributes.append(_test_attribute)

    return _test_attributes

def _get_comparisons(validations):
    _comparisons = list()
    for comparison in validations:
        _comparisons.append(comparison)

    return _comparisons

def generate_url(hostname, attributes):
    _url = 'https://{0}{1}'
    _url = _url.format(hostname, attributes.url)

    return _url
