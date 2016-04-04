from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class RestTestGet(AbstractRestTest):

    def __init__(self, url, headers, comparisons):
        self.url = url
        self.headers = headers
        self.comparisons = comparisons

    def get_response(self):
        #url = self._create_url()
        # consider getting this data from a yaml file
        #headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web', 'Accept': 'application/json'}
        r = requests.get(self.url, verify=False, headers=self.headers)
        return r

    def additional_response_verification(self, response):
        super(RestTestGet, self).additional_response_verification(response)
