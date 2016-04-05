import json
import collections

class JsonVerification:

    _json_messages_from_get_all = None

    def __init__(self, response, comparisons):
        self.response = response
        self.comparisons = comparisons

    def _retrieve_key_from_comparison(self, comparison):
        ComparisonAttributes = collections.namedtuple('ComparisonAttributes', ['key', 'value',
                                                                               'expected',
                                                                               'comparator'])
        #there is only one key per compare, all other attributes are of informational or expected
        #values, etc
        for attribute in comparison:
            if attribute != 'expected' and attribute != 'comparator':
                print('_retrieved key is:', attribute)
                print('_retrieved key value is:', comparison[attribute])
                print('_retrieved expected value:', comparison['expected'])
                print('_retrieved comparator value:', comparison['comparator'])
                _comparison_attributes = ComparisonAttributes(attribute, comparison[attribute],
                                                              comparison['expected'],
                                                              comparison['comparator'])

    def _get_all(self, myjson, key):
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    if jsonkey == key:
                        #print('in _get_all function')
                        #print(str(myjson[jsonkey]))
                        self._json_messages_from_get_all.append(myjson[jsonkey])
                    self._get_all(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self._get_all(item, key)

    def _validate_each_comparison(self, comparison, list_of_json):
        print("comparison to use:", comparison)
        for json in list_of_json:
            print('_validate_each_comparison:', json)

    def validate(self):
        for comparison in self.comparisons:
            comparison_value = comparison['compare']
            self._json_messages_from_get_all = list()
            json_messages_from_get_all  = list()
            key = self._retrieve_key_from_comparison(comparison_value)
            self._get_all(self.response, 'messages')
            self._validate_each_comparison(comparison_value, self._json_messages_from_get_all)


