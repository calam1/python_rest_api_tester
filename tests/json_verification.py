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
                #print('_retrieved key is:', attribute)
                #print('_retrieved key value is:', comparison[attribute])
                #print('_retrieved expected value:', comparison['expected'])
                #print('_retrieved comparator value:', comparison['comparator'])
                _comparison_attributes = ComparisonAttributes(attribute, comparison[attribute],
                                                              comparison['expected'],
                                                              comparison['comparator'])
                return _comparison_attributes

    def _get_all_matching(self, myjson, key):
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    if jsonkey == key:
                        #print('in _get_all_matching function')
                        #print(str(myjson[jsonkey]))
                        self._json_messages_from_get_all_matching.append(myjson[jsonkey])
                    self._get_all_matching(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self._get_all_matching(item, key)

    def _validate_each_comparison(self, comparison_attribute, list_of_json):
        _attribute_value = comparison_attribute.value
        _expected = comparison_attribute.expected

        for json in list_of_json:
            if str(json[_attribute_value]) != _expected:
                print('Comparison failed, the actual value expected does not match the expected')
                print('value', str(json[_attribute_value]))
                print('expected', _expected)
            else:
                print("value matches expected")

    def validate(self):
        for comparison in self._comparisons:
            comparison_value = comparison['compare']
            self._json_messages_from_get_all_matching = list()
            comparison_attribute = self._retrieve_key_from_comparison(comparison_value)
            key = comparison_attribute.key
            self._get_all_matching(self._response, key)
            self._validate_each_comparison(comparison_attribute, self._json_messages_from_get_all_matching)

