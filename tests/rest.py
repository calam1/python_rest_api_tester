from abc import ABCMeta, abstractmethod
import os
import requests
import status_check

class AbstractRestTest(object):

    # to enforce the abstract class
    __metaclass__=ABCMeta

    def test_web_service(self):
        r = self.get_response()
        status_check.check_statuses(r)
        self.additional_response_verification(r)
        return r

    # just prints the found key, need to add to a collection 
    #def _get_all(myjson, key):
    #    if type(myjson) == str:
    #        myjson = json.loads(myjson)
    #    if type(myjson) is dict:
    #        for jsonkey in myjson:
    #            if type(myjson[jsonkey]) in (list, dict):
    #                if jsonkey == key:
    #                    print(str(myjson[jsonkey]))
    #                get_all(myjson[jsonkey], key)
    #    elif type(myjson) is list:
    #        for item in myjson:
    #            if type(item) in (list, dict):
    #                get_all(item, key)

    # add hook to do additional response verification
    @abstractmethod
    def additional_response_verification(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        print('what is comparisons value', self.comparisons)

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass

