import open_and_load_config
from rest_get import RestTestGet

def init():
    _cfg = open_and_load_config.open_and_load_yaml_file()

    # _hostname and _headers are common among all tests
    _hostname = open_and_load_config.get_host_name(_cfg)
    _headers = open_and_load_config.get_headers(_cfg)

    # a collection of different tests, with their respective REST urls, etc
    _attributes = open_and_load_config.get_test_attributes(_cfg)

    # will hold a collection of tests objects containing all their info and results
    _rest_test_get_results = list()

    for attr in _attributes:
        _restful_url = open_and_load_config.generate_url(_hostname, attr)
        # when we do the POST we want to create a factory
        # also multi thread this, use the ThreadPoolExecutor
        _rest_get = RestTestGet(attr.name, _restful_url, _headers, attr.comparisons)
        _response = _rest_get.test_web_service()
        _rest_test_get_results.append(_rest_get)
        #print(_response)

# This is temporary or maybe for just command line, maybe we filter out all the failures and show
# those only, not sure for now
    # list of RestTestGet objects
    for rest_test_get in _rest_test_get_results:
        # each object's list of validation results
        _rest_tests = rest_test_get._results
        # iterate through the list and print it for now
        for results in _rest_tests:
            print('The test we ran is named: {} and the URL is: {} and it passed: {}, the message was: {}'.format(rest_test_get._name, rest_test_get._url, results.isPass, results.message))

init()
