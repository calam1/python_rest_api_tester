from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestGet(AbstractRestTest):

    def __init__(self, name, url, headers, comparisons):
        self.name = name
        self.url = url
        self.results = None
        self.headers = headers
        self.comparisons = comparisons
        self.results = None

    def get_response(self):
        response = requests.get(self.url, verify=False, headers=self.headers)
        return response

    def additional_response_validation(self, response):
        super(RestTestGet, self).additional_response_validation(response)
