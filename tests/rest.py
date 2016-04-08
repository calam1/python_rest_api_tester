from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import status_check
import collections

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__= ABCMeta

    def test_web_service(self):
        r = self.get_response()
        print('Testing the following web service:', self._name)
        # do we want to add the default check to the named tuple like we do for the add'l
        # validationss
        status_check.check_statuses(r)
        self.additional_response_validation(r)
        return r

    # print for now, but create a tuple/object that contains the name of the test, comparisons, etc,
    # whatever makes sense, think it through
    # maybe just set the proper message per compare back into the RestTestGet object
    def _manage_results(self, comparison_results):
        ComparisonResults = collections.namedtuple('ComparisonResults', ['isPass', 'message'])
        _result_status_messages = list()

        for messages in comparison_results:
            _comparison_results = None
            if messages.get('success') != None:
                print(messages.get('success'))
                _comparison_results = ComparisonResults(True, messages.get('success'))
            elif messages.get('failure_wrong_value') != None:
                print(messages.get('failure_wrong_value'))
                _comparison_results = ComparisonResults(False, messages.get('failure_wrong_value'))
            elif messages.get('failure_no_value') != None:
                print(messages.get('failure_no_value'))
                _comparison_results = ComparisonResults(True, messages.get('failure_no_value'))
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
        _result_status_message = self._manage_results(_verification_results)
        self._results = _result_status_message

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

