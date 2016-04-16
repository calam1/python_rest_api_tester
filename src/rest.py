from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import comparison_result_factory
import re

class AbstractRestTest(object):

    __metaclass__ = ABCMeta

    def test_web_service(self):
        if self.prep_state_tests:
            resps = [rest_test.test_web_service() for rest_test in self.prep_state_tests]
            print('Prep state results')
            print('Test named:', self.name, 'has this REST api called before itself:', self.prep_state_tests[0].name,  self.prep_state_tests[0].results)

        response = self.get_response()
        bad_status = self._check_status_code(response)
        # if status code is bad, no need to do additional validation
        if bad_status is not None:
            return response
        else:
            self.additional_response_validation(response)
            return response

    def _manage_results(self, comparison_results):
        return [comparison_result_factory.build_comparison_result(messages) for messages in comparison_results]

    def _check_status_code(self, response):
        if response.status_code != 200:
            result_status_messages = list()
            response_status_code_error = 'Error occurred, service has an issue, response code is: {}'.format(
                response.status_code)
            response_error_results = comparison_result_factory.ComparisonResults(False, response_status_code_error)
            result_status_messages.append(response_error_results)
            # set error message to test object, additional_repsonse_validation will not run, so we
            # need to set the failure value
            self.results = result_status_messages
            return result_status_messages

        # this should not exist for any web service, except for the incorrect way we implemented it
        return self._odd_error(response)

    def _odd_error(self, response):
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
            self.results = result_status_messages

        return result_status_messages

    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        json_verification = JsonVerification(utf_8_response, self.comparisons)
        verification_results = json_verification.validate()
        result_status_message = self._manage_results(verification_results)
        self.results = result_status_message

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass
