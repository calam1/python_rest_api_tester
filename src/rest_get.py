from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestGet(AbstractRestTest):

    def __init__(self, name, prep_state_tests, url, headers, comparisons):
        self.name = name
        self.prep_state_tests = prep_state_tests
        self.url = url
        self.headers = headers
        self.comparisons = comparisons
        self.cookies = None
        self.results = None

    def get_response(self):
        response = requests.get(self.url, verify=False, headers=self.headers, cookies=self.cookies)
        return response

    def additional_response_validation(self, response):
        super(RestTestGet, self).additional_response_validation(response)
