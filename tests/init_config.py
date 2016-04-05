import os
import yaml
import collections
from rest_get import RestTestGet

def _open_and_load_yaml_file():
    _config_dir = os.path.dirname(__file__)
    _rel_path = 'config.yml'
    _abs_file_path = os.path.join(_config_dir, _rel_path)

    with open(_abs_file_path, 'r') as ymlfile:
        _cfg = yaml.load(ymlfile)

    return _cfg

def _get_host_name(cfg):
    _configs = cfg[0]
    _config_list = _configs['config']
    _hostname = None
    for c in _config_list:
        _hostname = c['hostname']

    return _hostname

def _get_headers(cfg):
    _common_settings = cfg[1]
    _headers = None
    for common_setting in _common_settings:
        _cs = _common_settings[common_setting]
        for c in _cs:
            _headers = c['headers']

    return _headers

def _get_test_attributes(cfg):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'url', 'method',
                                                               'comparisons'])

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

        for params in _test:
            _key = params.keys()[0]
            if _key == 'name':
                _name = params[_key]

            if _key == 'url':
                _url = params[_key]

            if _key == 'method':
                _method = params[_key]

            if _key == 'validations':
                _validations = params[_key]
                _comparisons = _get_comparisons(_validations)

        _test_attribute = TestAttributes(_name, _url, _method, _comparisons)
        _test_attributes.append(_test_attribute)

    return _test_attributes

def _get_comparisons(validations):
    _comparisons = list()
    for comparison in validations:
        _comparisons.append(comparison)

    return _comparisons

def _generate_url(hostname, attributes):
    _url = 'https://{0}{1}'
    _url = _url.format(hostname, attributes.url)

    return _url

def init():
    _cfg = _open_and_load_yaml_file()

    # _hostname and _headers are common among all tests
    _hostname = _get_host_name(_cfg)
    _headers = _get_headers(_cfg)

    # a collection of different tests, with their respective REST urls, etc
    _attributes = _get_test_attributes(_cfg)

    for a in _attributes:
        _restful_url = _generate_url(_hostname, a)
        # when we do the POST we want to create a factory
        _rest_get = RestTestGet(_restful_url, _headers, a.comparisons)

        #for c in a.comparisons:
        #    print('chris', c)

        _response = _rest_get.test_web_service()
        print(_response)

init()
