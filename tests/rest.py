from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import os
import requests
import status_check

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__= ABCMeta

    def test_web_service(self):
        r = self.get_response()
        print('Testing the following web service:', self._name)
        status_check.check_statuses(r)
        self.additional_response_validation(r)
        return r

    # print for now, but create a tuple/object that contains the name of the test, comparisons, etc,
    # whatever makes sense, think it through
    def _manage_results(self, comparison_results):
        for messages in comparison_results:
            if messages.get('success') != None:
                print(messages.get('success'))
            elif messages.get('failure_wrong_value') != None:
                print(messages.get('failure_wrong_value'))
            elif messages.get('failure_no_value') != None:
                print(messages.get('failure_no_value'))
            else:
                raise Exception('Something bad happened, there should be a message')

    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        json_verification = JsonVerification(utf_8_response, self._comparisons)
        _verification_results = json_verification.validate()
        self._manage_results(_verification_results)

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

