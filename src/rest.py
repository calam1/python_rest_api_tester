from abc import ABCMeta, abstractmethod
from json_verification import JsonVerification
import comparison_result_factory
import check_basic_response


class AbstractRestTest(object):
    __metaclass__ = ABCMeta

    def test_web_service(self):
        # this is used in the case we depend on state on the server side in the session
        pipeline_session_uuid = None

        if self.prep_state_tests:
            # didn't use list comprehension here becasue I needed the pipeline session UUID for each
            # test_web_service() call, maybe there is a way to do it with list comprehension
            for rest_test in self.prep_state_tests:
                resp = rest_test.test_web_service()
                pipeline_session_uuid = resp.json().get('dataset').get('pipelineSession').get('values').get(
                    'pipeline_session_uuid')

        if pipeline_session_uuid:
            self.cookies = dict(PIPELINE_SESSION_ID=str(pipeline_session_uuid))

        response = self.get_response()
        bad_status = self.results = check_basic_response.check_status_code(response)
        # if status code is bad, no need to do additional validation
        if bad_status is not None:
            return response
        else:
            self.additional_response_validation(response)
            return response

    def _manage_results(self, comparison_results):
        return [comparison_result_factory.build_comparison_result(messages) for messages in comparison_results]

    @abstractmethod
    def additional_response_validation(self, response):
        resp_text = response.text
        utf_8_response = resp_text.encode('utf8')
        json_verification = JsonVerification(utf_8_response, self.comparisons)
        verification_results = json_verification.validate()
        result_status_message = self._manage_results(verification_results)
        self.results = result_status_message

    # define the verb, get, put, delete, etc
    @abstractmethod
    def get_response(self):
        pass
