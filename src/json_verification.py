import collections
from filter_json import FilterJson
from validate_comparison import ValidateComparison

class JsonVerification:

    def __init__(self, response, comparisons):
        self.response = response
        if comparisons is None:
            self.comparisons = list()
        else:
            self.comparisons = comparisons

    def _retrieve_comparisons(self, comparison):
        ComparisonAttributes = collections.namedtuple('ComparisonAttributes', ['key', 'value', 'expected', 'comparator'])

        #there is only one key per compare, all other attributes are of informational or expected values, etc
        key = filter(lambda a: a != 'expected' and a != 'comparator', comparison)
        for k in key:
            comparison_attributes = ComparisonAttributes(k, comparison[k], comparison['expected'], comparison['comparator'])
            return comparison_attributes

    def _get_comparison(self, comparison):
            comparison_value = comparison['compare']
            comparison_attribute = self._retrieve_comparisons(comparison_value)
            return comparison_attribute

    def validate(self):
        list_of_results_from_comparisons = list()

        # this is a collection of the compare yamls in the config.yml file
        for comparison in self.comparisons:
            comparison_attribute = self._get_comparison(comparison)
            filter_json = FilterJson()
            filtered_json = filter_json.filter_json(self.response, comparison_attribute.key)
            validate_comparison = ValidateComparison()
            map_of_messages = validate_comparison.validate_against_response(comparison_attribute, filtered_json)
            list_of_results_from_comparisons.append(map_of_messages)

        return list_of_results_from_comparisons
