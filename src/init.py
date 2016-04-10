import open_and_load_config
import collections
from rest_get import RestTestGet

def init():
    # load the yaml config
    _cfg = open_and_load_config.open_and_load_yaml_file()

    # _hostname and _headers are common among all tests
    _hostname = open_and_load_config.get_host_name(_cfg)
    _headers = open_and_load_config.get_headers(_cfg)

    # a collection of different tests, with their respective REST urls, etc
    _attributes = open_and_load_config.get_test_attributes(_cfg)

    # will hold a collection of tests objects containing all their test info and results
    _rest_test_get_results = _run_tests(_attributes, _hostname, _headers)

    # list to hold RestAPITestResult objects, which is basically every compare in the config.yml and
    # its test name and url
    _list_of_all_results = _assemble_results_with_test_attributes(_rest_test_get_results)

    # print results to the console
    _process_results_for_console(_list_of_all_results)

def _run_tests(attributes, hostname, headers):
    _rest_test_get_results = list()
    # looping through the loaded yaml file and running the tests and saving the results off
    for attr in attributes:
        _restful_url = open_and_load_config.generate_url(hostname, attr)
        # when we do the POST we want to create a factory to return RestTestGet, TestTestPost, etc
        # also multi thread this, use the ThreadPoolExecutor
        _rest_get = RestTestGet(attr.name, _restful_url, headers, attr.comparisons)
        _response = _rest_get.test_web_service()
        _rest_test_get_results.append(_rest_get)

    return _rest_test_get_results

def _assemble_results_with_test_attributes(rest_test_get_results):
    _list_of_all_results = list()

    # assembling the results with the tests that they are associated with
    RestAPITestResult = collections.namedtuple('RestAPITestResult', ['name', 'url', 'isPass', 'message'])

    # list of RestTestGet objects
    for rest_test_get in rest_test_get_results:
        # each object's list of validation results
        _rest_tests = rest_test_get.results
        for results in _rest_tests:
            _rest_api_test_result = RestAPITestResult(rest_test_get.name, rest_test_get.url, results.isPass, results.message)
            _list_of_all_results.append(_rest_api_test_result)

    return _list_of_all_results

def _process_results_for_console(list_of_all_results):
    # print results to the console
    print('---------------------------- FAILURES ---------------------------------')
    _failures = filter(lambda x: x.isPass is False, list_of_all_results)
    for results in _failures:
        print('The test we ran is named: {} and the URL is: {} and it passed: {}, the message was: {}'.format(results.name, results.url, results.isPass, results.message))

    print('---------------------------- SUCCESSES ---------------------------------')
    _success = filter(lambda x: x.isPass is True, list_of_all_results)
    for results in _success:
        print('The test we ran is named: {} and the URL is: {} and it passed: {}, the message was: {}'.format(results.name, results.url, results.isPass, results.message))


init()
