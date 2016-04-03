from abc import ABCMeta, abstractmethod
from rest import AbstractRestTest
import requests

class AbstractRestTestGet(AbstractRestTest):

    # to enforce the abstract class
    __metaclass__=ABCMeta

    def get_response(self):
        url = self._create_url()
        # consider getting this data from a yaml file
        headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web', 'Accept': 'application/json'}
        r = requests.get(url, verify=False, headers=headers)
        return r
