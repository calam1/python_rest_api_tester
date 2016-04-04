from abc import ABCMeta, abstractmethod
import os
import requests
import status_check

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__=ABCMeta

    def test_web_service(self):
        self.set_up_web_service_test()
        r = self.get_response()
        status_check.check_statuses(r)
        self.additional_response_verification(r)

    # add hook to do additional set up, such as add to cart for checkout, etc
    def set_up_web_service_test(self):
        pass

    # add hook to do additional response verification
    def additional_response_verification(self, response):
        pass

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

