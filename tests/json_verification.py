import json
import collections

class JsonVerification:

    def __init__(self, response, comparisons):
        self._response = response
        self._comparisons = comparisons
        self._json_messages_from_get_all_matching = None

    def _retrieve_key_from_comparison(self, comparison):
        ComparisonAttributes = collections.namedtuple('ComparisonAttributes', ['key', 'value',
                                                                               'expected',
                                                                               'comparator'])
        #there is only one key per compare, all other attributes are of informational or expected
        #values, etc
        for attribute in comparison:
            if attribute != 'expected' and attribute != 'comparator':
                _comparison_attributes = ComparisonAttributes(attribute, comparison[attribute],
                                                              comparison['expected'],
                                                              comparison['comparator'])
                return _comparison_attributes

    def _get_all_matching_values_from_response(self, myjson, key):
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    if jsonkey == key:
                        self._json_messages_from_get_all_matching.append(myjson[jsonkey])
                    self._get_all_matching_values_from_response(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self._get_all_matching_values_from_response(item, key)

    def _match(self, myjson, key):
        if type(myjson) == str:
            print('json is a string')
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for k, v in myjson.items():
                if str(k) == key:
                    return str(v)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    return self._match(item, key)

    def _validate_each_comparison(self, comparison_attribute, list_of_json):
        _attribute_value = comparison_attribute.value
        _expected = comparison_attribute.expected

        _local_messages = dict()

        for json in list_of_json:
            if isinstance(json, dict) and str(json.get(_attribute_value)) != _expected:
                if json.get(_attribute_value) != None:
                    _failure_msg = 'Comparison failed, the actual value expected does not match the expected actual value: {}, expected value: {}'.format(json.get(_attribute_value), _expected)
                    _local_messages['failure_wrong_value'] = _failure_msg
                else:
                    _failure_msg = 'Comparison failed, the actual value does not exist, the expected value: {}'.format(_expected)
                    _local_messages['failure_no_value'] = _failure_msg

            elif isinstance(json, list):
                _key_value = self._match(json, comparison_attribute.value)
                if _key_value == _expected:
                    _success_msg = 'actual value: {} matches expected value: {}'.format(_key_value, _expected)
                    _local_messages['success'] = _success_msg
                elif _key_value != None:
                    _failure_msg = 'Comparison failed, the actual value expected does not match the expected, actual: {}, expected: {}'.format(_key_value, _expected)
                    _local_messages['failure_wrong_value'] = _failure_msg
                else:
                    _failure_msg = 'Comparison failed, the actual value does not exist, the expected value {}'.format(_expected)
                    _local_messages['failure_no_value'] = _failure_msg
            else:
                _success_msg = 'actual value: {} matches expected value: {}'.format(json.get(_attribute_value), _expected)
                _local_messages['success'] = _success_msg

        return _local_messages

    def validate(self):
        # this is a collection of comparisons in the yaml file
        for comparison in self._comparisons:
            comparison_value = comparison['compare']
            self._json_messages_from_get_all_matching = list()
            comparison_attribute = self._retrieve_key_from_comparison(comparison_value)
            key = comparison_attribute.key
            self._get_all_matching_values_from_response(self._response, key)
            _map_of_messages = self._validate_each_comparison(comparison_attribute, self._json_messages_from_get_all_matching)
            if _map_of_messages.get('success') != None:
                print(_map_of_messages.get('success'))
            elif _map_of_messages.get('failure_wrong_value') != None:
                print(_map_of_messages.get('failure_wrong_value'))
            elif _map_of_messages.get('failure_no_value') != None:
                print(_map_of_messages.get('failure_no_value'))
            else:
                raise Exception('Something bad happened, there should be a message')

