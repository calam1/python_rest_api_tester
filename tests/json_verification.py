import json
import collections

class JsonVerification:

    def __init__(self, response, comparisons):
        self._response = response
        self._comparisons = comparisons
        self._json_messages_from_get_all_matching = None
        self._actual_value = None

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
                        #print('in _get_all_matching function')
                        #print(str(myjson[jsonkey]))
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
            for jsonkey in myjson:
                if str(jsonkey) == key:
                    #print(str(myjson.get(jsonkey)))
                    self._actual_value = str(myjson.get(jsonkey))
                self._match(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self._match(item, key)


    def _validate_each_comparison(self, comparison_attribute, list_of_json):
        _attribute_value = comparison_attribute.value
        _expected = comparison_attribute.expected

        for json in list_of_json:
            if isinstance(json, dict) and str(json.get(_attribute_value)) != _expected:
                print('Comparison failed, the actual value expected does not match the expected')
                print('actual {}, expected {}'.format(json.get(_attribute_value), _expected))
            elif isinstance(json, list):
                self._match(json, comparison_attribute.value)
                if self._actual_value == _expected:
                    print('actual value {} matches expected value {}'.format(self._actual_value, _expected))
            else:
                print('actual value {} matches expected value {}'.format(json.get(_attribute_value), _expected))

    def validate(self):
        # this is a collection of comparisons in the yaml file
        for comparison in self._comparisons:
            comparison_value = comparison['compare']
            self._json_messages_from_get_all_matching = list()
            comparison_attribute = self._retrieve_key_from_comparison(comparison_value)
            key = comparison_attribute.key
            self._get_all_matching_values_from_response(self._response, key)
            self._validate_each_comparison(comparison_attribute, self._json_messages_from_get_all_matching)

