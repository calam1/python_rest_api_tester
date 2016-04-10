from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestGet(AbstractRestTest):

    def __init__(self, name, url, headers, comparisons):
        self.name = name
        self.url = url
        self.results = None
        self._headers = headers
        self._comparisons = comparisons
        self.results = None

    def get_response(self):
        _r = requests.get(self.url, verify=False, headers=self._headers)
        return _r

    def additional_response_validation(self, response):
        super(RestTestGet, self).additional_response_validation(response)
