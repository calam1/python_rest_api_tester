import json

class ValidateComparison:

    def __init__(self):
        self.local_messages = dict()
        # TODO figure how to do constants correctly
        self.FAILURE_NO_VALUE = 'failure_no_value'
        self.FAILURE_WRONG_VALUE = 'failure_wrong_value'
        self.SUCCESS = 'success'

    def _match(self, myjson, key):
        if type(myjson) is dict:
            for k, v in myjson.items():
                if k == key:
                    return v
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    return self._match(item, key)

    def validate_against_response(self, comparison_attribute, list_of_json):
        if list_of_json is None or len(list_of_json) == 0:
            self.local_messages[self.FAILURE_NO_VALUE] = 'No json key found.'
            return self.local_messages

        attribute_value = comparison_attribute.value
        expected = comparison_attribute.expected

        for json in list_of_json:
            if isinstance(json, dict) and json.get(attribute_value) != expected:
                self._populate_actual_not_equal_expected_failure_messages(json, attribute_value, expected)
            elif isinstance(json, list):
                self._iterate_list_find_matching_value_populate_result_message(json, comparison_attribute, expected)
            elif json.get(attribute_value) == expected:
                self._populate_actual_matches_expected_message(json, attribute_value, expected)

        return self.local_messages

    def _populate_actual_not_equal_expected_failure_messages(self, json, attribute_value, expected):
        if json.get(attribute_value) != None:
            failure_msg = 'Comparison failed, the actual value expected does not match the expected actual value: {}, expected value: {}'.format(json.get(attribute_value), expected)
            self.local_messages[self.FAILURE_WRONG_VALUE] = failure_msg
        else:
            failure_msg = 'Comparison failed, the actual value does not exist, the expected value: {}'.format(expected)
            self.local_messages[self.FAILURE_NO_VALUE] = failure_msg

    def _iterate_list_find_matching_value_populate_result_message(self, json, comparison_attribute, expected):
        key_value = self._match(json, comparison_attribute.value)
        if key_value == expected:
            success_msg = 'actual value: {} matches expected value: {}'.format(key_value, expected)
            self.local_messages[self.SUCCESS] = success_msg
        elif key_value != None:
            failure_msg = 'Comparison failed, the actual value expected does not match the expected, actual: {}, expected: {}'.format(key_value, expected)
            self.local_messages[self.FAILURE_WRONG_VALUE] = failure_msg
        else:
            failure_msg = 'Comparison failed, the actual value does not exist, the expected value {}'.format(expected)
            self.local_messages[self.FAILURE_NO_VALUE] = failure_msg

    def _populate_actual_matches_expected_message(self, json, attribute_value, expected):
        success_msg = 'actual value: {} matches expected value: {}'.format(json.get(attribute_value), expected)
        self.local_messages[self.SUCCESS] = success_msg
