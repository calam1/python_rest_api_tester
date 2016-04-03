from rest_get import AbstractRestTestGet

class Search(AbstractRestTestGet):

    def get_url(self):
        # consider putting this in yaml
        return 'https://{0}/services/search/duvet.do'

    def set_up_web_service_test(self):
        print('DO PRE SETUP FOR WEB SERVICE TEST')

    def additional_response_verification(self, response):
        print("DO ADDITIONAL RESPONSE VERIFICATION")
