import json

class ValidateComparison:

    def __init__(self):
        self._local_messages = dict()

    def _match(self, myjson, key):
        #if type(myjson) == str:
        #    print('json is a string')
        #    myjson = json.loads(myjson)
        if type(myjson) is dict:
            for k, v in myjson.items():
                if k == key:
                    return v
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    return self._match(item, key)

    def validate_against_response(self, comparison_attribute, list_of_json):
        _attribute_value = comparison_attribute.value
        _expected = comparison_attribute.expected

        if list_of_json is None or len(list_of_json) == 0:
            self._local_messages['failure_no_value'] = 'No json key found.'
            return self._local_messages

        for json in list_of_json:
            # hopefully I can abstract out this ugliness into a Factory when I build an object
            # containing all the info I want per test, otherwise this is a bit ugly
            if isinstance(json, dict) and json.get(_attribute_value) != _expected:
                if json.get(_attribute_value) != None:
                    _failure_msg = 'Comparison failed, the actual value expected does not match the expected actual value: {}, expected value: {}'.format(json.get(_attribute_value), _expected)
                    self._local_messages['failure_wrong_value'] = _failure_msg
                else:
                    _failure_msg = 'Comparison failed, the actual value does not exist, the expected value: {}'.format(_expected)
                    self._local_messages['failure_no_value'] = _failure_msg
            elif isinstance(json, list):
                _key_value = self._match(json, comparison_attribute.value)
                if _key_value == _expected:
                    _success_msg = 'actual value: {} matches expected value: {}'.format(_key_value, _expected)
                    self._local_messages['success'] = _success_msg
                elif _key_value != None:
                    _failure_msg = 'Comparison failed, the actual value expected does not match the expected, actual: {}, expected: {}'.format(_key_value, _expected)
                    self._local_messages['failure_wrong_value'] = _failure_msg
                else:
                    _failure_msg = 'Comparison failed, the actual value does not exist, the expected value {}'.format(_expected)
                    self._local_messages['failure_no_value'] = _failure_msg
            else:
                _success_msg = 'actual value: {} matches expected value: {}'.format(json.get(_attribute_value), _expected)
                self._local_messages['success'] = _success_msg

        return self._local_messages
