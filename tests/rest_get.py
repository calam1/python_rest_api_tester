from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestGet(AbstractRestTest):

    def __init__(self, name, url, headers, comparisons):
        self._name = name
        self._url = url
        self._headers = headers
        self._comparisons = comparisons
        self._results = None

    def get_response(self):
        _r = requests.get(self._url, verify=False, headers=self._headers)
        return _r

    def additional_response_validation(self, response):
        super(RestTestGet, self).additional_response_validation(response)
