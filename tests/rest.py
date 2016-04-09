from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import collections
import re

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__= ABCMeta

    def test_web_service(self):
        _response = self.get_response()
        print('Testing the following web service:{} and the url is {}'.format(self._name, self._url))
        self.additional_response_validation(_response)
        return _response

    def _manage_results(self, response, comparison_results):
        ComparisonResults = collections.namedtuple('ComparisonResults', ['isPass', 'message'])
        _result_status_messages = list()

        if response.status_code != 200:
            response_status_code_error = 'Error occurred, service has an issue, response code is: {}'.format(response.status_code)
            print(response_status_code_error)
            _response_error_results = ComparisonResults(False, response_status_code_error)
            _result_status_messages.append(_response_error_results)
            return _result_status_messages

        # due to the crappy way we implemented web services we almost always get a 200 unless the
        # server is down
        _resp_text = response.text
        _is_not_found = re.search('not_found.jsp', _resp_text)
        if _is_not_found is not None:
            _response_error_results = ComparisonResults(False, 'Web Service is not found.')
            _result_status_messages.append(_response_error_results)

        for messages in comparison_results:
            # this can probably be encapsulated into a factory
            _comparison_results = None
            if messages.get('success') != None:
                _comparison_results = ComparisonResults(True, messages.get('success'))
            elif messages.get('failure_wrong_value') != None:
                _comparison_results = ComparisonResults(False, messages.get('failure_wrong_value'))
            elif messages.get('failure_no_value') != None:
                _comparison_results = ComparisonResults(False, messages.get('failure_no_value'))
            else:
                raise Exception('Something bad happened, there should be a message')

            _result_status_messages.append(_comparison_results)

        return _result_status_messages

    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        _json_verification = JsonVerification(utf_8_response, self._comparisons)
        _verification_results = _json_verification.validate()
        _result_status_message = self._manage_results(response, _verification_results)
        self._results = _result_status_message

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

