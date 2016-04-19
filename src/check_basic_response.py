import comparison_result_factory
import re

def check_status_code(response):
    if response.status_code != 200:
        result_status_messages = list()
        response_status_code_error = 'Error occurred, service has an issue, response code is: {}'.format(
            response.status_code)
        response_error_results = comparison_result_factory.ComparisonResults(False, response_status_code_error)
        result_status_messages.append(response_error_results)
        # set error message to test object, additional_repsonse_validation will not run, so we
        # need to set the failure value
        return result_status_messages

    # this should not exist for any web service, except for the incorrect way we implemented it
    return _odd_error(response)


def _odd_error(response):
    # due to the crappy way we implemented web services we almost always get a 200 unless the
    # server is down, this should be a special branch and not in master
    # so you have to check for something all the time for our services, since http return code
    # is not accurate
    result_status_messages = None

    resp_text = response.text
    is_not_found = re.search('not_found.jsp', resp_text)
    if is_not_found is not None:
        result_status_messages = list()
        response_error_results = comparison_result_factory.ComparisonResults(False, 'Web Service is not found.')
        result_status_messages.append(response_error_results)

    return result_status_messages
