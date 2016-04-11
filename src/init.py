import open_and_load_config
import collections
from rest_get import RestTestGet


def main():
    # load the yaml config
    cfg = open_and_load_config.open_and_load_yaml_file()

    # hostname and headers are common among all tests
    hostname = open_and_load_config.get_host_name(cfg)
    headers = open_and_load_config.get_headers(cfg)

    # a collection of different tests, with their respective REST urls, etc
    attributes = open_and_load_config.get_test_attributes(cfg)

    # will hold a collection of tests objects containing all their test info and results
    rest_test_get_results = _run_tests(attributes, hostname, headers)

    # list to hold RestAPITestResult objects, which is basically every compare in the config.yml and
    # its test name and url
    list_of_all_results = _assemble_results_with_test_attributes(rest_test_get_results)

    # print results to the console
    _process_results_for_console(list_of_all_results)


def _run_tests(attributes, hostname, headers):
    rest_tests = [RestTestGet(attr.name, open_and_load_config.generate_url(hostname, attr), headers, attr.comparisons)
                  for attr in attributes]
    [rest_test.test_web_service() for rest_test in rest_tests]
    return rest_tests


def _assemble_results_with_test_attributes(rest_test_get_results):
    list_of_all_results = list()

    # assembling the results with the tests that they are associated with
    RestAPITestResult = collections.namedtuple('RestAPITestResult', ['name', 'url', 'isPass', 'message'])

    # list of RestTestGet objects
    for rest_test_get in rest_test_get_results:
        # each object's list of validation results
        [list_of_all_results.append(
            [RestAPITestResult(rest_test_get.name, rest_test_get.url, results.isPass, results.message) for results in
             rest_test_get.results][counter]) for counter in range(len(rest_test_get.results))]

    return list_of_all_results


def _process_results_for_console(list_of_all_results):
    # print results to the console
    print('---------------------------- FAILURES ---------------------------------')
    failures = filter(lambda x: x.isPass is False, list_of_all_results)
    for results in failures:
        print(
        'The test we ran is named: {} and the URL is: {} and it passed: {}, the message was: {}'.format(results.name,
                                                                                                        results.url,
                                                                                                        results.isPass,
                                                                                                        results.message))

    print('---------------------------- SUCCESSES ---------------------------------')
    success = filter(lambda x: x.isPass is True, list_of_all_results)
    for results in success:
        print(
        'The test we ran is named: {} and the URL is: {} and it passed: {}, the message was: {}'.format(results.name,
                                                                                                        results.url,
                                                                                                        results.isPass,
                                                                                                        results.message))


if __name__ == '__main__':
    main()
