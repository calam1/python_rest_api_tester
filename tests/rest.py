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

    # add hook to do additional response verification
    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        json_verification = JsonVerification(utf_8_response, self._comparisons)
        json_verification.validate()

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

