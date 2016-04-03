from rest import AbstractRestTest

class Search(AbstractRestTest):

    def get_url(self):
        # consider putting this in yaml
        return 'https://{0}/services/search/duvet.do'

    def set_up_web_service_test(self):
        print('DO PRE SETUP FOR WEB SERVICE TEST')

    def additional_response_verification(self):
        print("DO ADDITIONAL RESPONSE VERIFICATION")
