import collections

def build_test_attributes(test):
    TestAttributes = collections.namedtuple('TestAttributes', ['name', 'prep_states', 'url', 'method', 'payload', 'comparisons'])

    prep_states = list()
    name = None
    url = None
    method = None
    payload = None
    comparisons = None

    for params in test:
        if (filter(lambda x: x == 'name', params)):
            name = params.values()[0]

        if (filter(lambda x: x == 'prep_state', params)):
            prep_state = params.values()[0]
            test_attribute = build_test_attributes(prep_state)
            prep_states.append(test_attribute)

        if len(filter(lambda x: x == 'url', params)):
            url = params.values()[0]

        if len(filter(lambda x: x == 'method', params)):
            method = params.values()[0]

        if len(filter(lambda x: x == 'payload', params)):
            payload = params.values()[0]

        if len(filter(lambda x: x == 'validations', params)):
            validations = params.values()[0]
            comparisons = _get_comparisons(validations)

    return TestAttributes(name, prep_states, url, method, payload, comparisons)


def _get_comparisons(validations):
    comparisons = list()
    for comparison in validations:
        comparisons.append(comparison)

    return comparisons
