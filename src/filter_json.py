import json

class FilterJson:

    def __init__(self):
        self.json_messages_from_get_all_matching = list()

    def filter_json(self, myjson, key):
        self._get_all_matching_values_from_response(myjson, key)
        return self.json_messages_from_get_all_matching

    #http://stackoverflow.com/questions/14048948/how-can-i-use-python-finding-particular-json-value-by-key
    def _get_all_matching_values_from_response(self, myjson, key):
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    if jsonkey == key:
                        self.json_messages_from_get_all_matching.append(myjson[jsonkey])
                    self._get_all_matching_values_from_response(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    self._get_all_matching_values_from_response(item, key)
