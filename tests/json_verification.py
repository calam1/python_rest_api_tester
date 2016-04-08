import collections
from filter_json import FilterJson
from validate_comparison import ValidateComparison

class JsonVerification:

    def __init__(self, response, comparisons):
        self._response = response
        self._comparisons = comparisons

    def _retrieve_comparisons(self, comparison):
        ComparisonAttributes = collections.namedtuple('ComparisonAttributes', ['key', 'value', 'expected', 'comparator'])
        #there is only one key per compare, all other attributes are of informational or expected values, etc
        for attribute in comparison:
            if attribute != 'expected' and attribute != 'comparator':
                _comparison_attributes = ComparisonAttributes(attribute, comparison[attribute], comparison['expected'], comparison['comparator'])
                return _comparison_attributes

    def _get_comparison(self, comparison):
            _comparison_value = comparison['compare']
            _comparison_attribute = self._retrieve_comparisons(_comparison_value)
            return _comparison_attribute

    def validate(self):
        _list_of_results_from_comparisons = list()

        # this is a collection of the compare yamls in the config.yml file
        for comparison in self._comparisons:
            _comparison_attribute = self._get_comparison(comparison)
            _filter_json = FilterJson()
            _filtered_json = _filter_json.filter_json(self._response, _comparison_attribute.key)
            _validate_comparison = ValidateComparison()
            _map_of_messages = _validate_comparison.validate_against_response(_comparison_attribute, _filtered_json)
            _list_of_results_from_comparisons.append(_map_of_messages)

        return _list_of_results_from_comparisons
