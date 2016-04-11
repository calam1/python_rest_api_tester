import collections

ComparisonResults = collections.namedtuple('ComparisonResults', ['isPass', 'message'])

def build_comparison_result(messages):
    if messages.get('success') != None:
        comparison_results = ComparisonResults(True, messages.get('success'))
    elif messages.get('failure_wrong_value') != None:
        comparison_results = ComparisonResults(False, messages.get('failure_wrong_value'))
    elif messages.get('failure_no_value') != None:
        comparison_results = ComparisonResults(False, messages.get('failure_no_value'))
    else:
        raise Exception('Something bad happened, there should be a message')

    return comparison_results
