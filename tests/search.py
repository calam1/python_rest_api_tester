from rest import AbstractRestTest

class Search(AbstractRestTest):

    def get_url(self):
        # consider putting this in yaml
        return 'https://{0}/services/search/duvet.do'
