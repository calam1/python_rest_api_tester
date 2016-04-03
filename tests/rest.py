from abc import ABCMeta, abstractmethod
import os
import requests
import status_check

class AbstractRestTest(object):

    #to enforce the abstract class
    __metaclass__=ABCMeta

    def _create_url(self):
        configuration_dir = os.path.dirname(__file__)
        relative_path = 'config.txt'
        abs_file_path = os.path.join(configuration_dir, relative_path)

        with open(abs_file_path) as f:
            for dns in f:
               url = self.get_url() 
               url = url.format(dns.rstrip())

        return url

    def _get_response(self):
        url = self._create_url()
        # consider getting this data from a yaml file
        headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web', 'Accept': 'application/json'}
        r = requests.get(url, verify=False, headers=headers)
        return r

    def test_web_service(self):
        self.set_up_web_service_test()
        r = self._get_response()
        status_check.check_statuses(r)
        self.additional_response_verification()

    # add hook to do additional set up, such as add to cart for checkout, etc
    def set_up_web_service_test(self):
        pass

    # add hook to do additional response verification
    def additional_response_verification(self):
        pass

    @abstractmethod
    def get_url(self):
        pass
