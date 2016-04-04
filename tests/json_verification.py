class JsonVerification:

    def __init__(self, response, comparisons):
        self.response = response
        self.comparisons = comparisons

    # just prints the found key, need to add to a collection 
    def _get_all(myjson, key):
        if type(myjson) == str:
            myjson = json.loads(myjson)
        if type(myjson) is dict:
            for jsonkey in myjson:
                if type(myjson[jsonkey]) in (list, dict):
                    if jsonkey == key:
                        print(str(myjson[jsonkey]))
                    get_all(myjson[jsonkey], key)
        elif type(myjson) is list:
            for item in myjson:
                if type(item) in (list, dict):
                    get_all(item, key)

    def validate():
        pass
