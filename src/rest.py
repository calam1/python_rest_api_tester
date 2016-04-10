from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import comparison_result_factory
import re

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__= ABCMeta

    def test_web_service(self):
        _response = self.get_response()
        _bad_status = self._check_status_code(_response)
        # if status code is bad, no need to do additional validation
        if _bad_status is not None:
            return _response
        else:
            self.additional_response_validation(_response)
            return _response

    def _manage_results(self, response, comparison_results):
        _result_status_messages = list()

        for messages in comparison_results:
            _comparison_result = comparison_result_factory.build_comparison_result(messages)
            _result_status_messages.append(_comparison_result)

        return _result_status_messages

    def _check_status_code(self, response):
        _result_status_messages = None

        if response.status_code != 200:
            _result_status_messages = list()
            response_status_code_error = 'Error occurred, service has an issue, response code is: {}'.format(response.status_code)
            _response_error_results = comparison_result_factory.ComparisonResults(False, response_status_code_error)
            _result_status_messages.append(_response_error_results)
            # set error message to test object, additional_repsonse_validation will not run, so we
            # need to set the failure value
            self.results = _result_status_messages
            return _result_status_messages

        # this should not exist for any web service, except for the incorrect way we implemented it
        return self._odd_error(response)

    def _odd_error(self, response):
        # due to the crappy way we implemented web services we almost always get a 200 unless the
        # server is down, this should be a special branch and not in master
        # so you have to check for something all the time for our services, since http return code
        # is not accurate
        _result_status_messages = None

        _resp_text = response.text
        _is_not_found = re.search('not_found.jsp', _resp_text)
        if _is_not_found is not None:
            _result_status_messages = list()
            _response_error_results = comparison_result_factory.ComparisonResults(False, 'Web Service is not found.')
            _result_status_messages.append(_response_error_results)
            self.results = _result_status_messages

        return _result_status_messages

    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        _json_verification = JsonVerification(utf_8_response, self._comparisons)
        _verification_results = _json_verification.validate()
        _result_status_message = self._manage_results(response, _verification_results)
        self.results = _result_status_message

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

