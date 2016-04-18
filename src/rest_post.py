from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestPost(AbstractRestTest):

    def __init__(self, name, prep_state_tests, url, headers, payload, comparisons):
        self.name = name
        self.prep_state_tests = prep_state_tests
        self.url = url
        self.headers = headers
        self.payload = payload
        self.comparisons = comparisons
        self.cookies = None
        self.results = None

    def get_response(self):
        response = requests.post(self.url, verify=False, headers=self.headers, data=self.payload,
                                 cookies=self.cookies)
        return response

    def additional_response_validation(self, response):
        super(RestTestPost, self).additional_response_validation(response)
