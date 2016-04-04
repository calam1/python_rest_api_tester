import requests
import json
import os
import yaml

def init():
    dns = 'localhost:8443'
    url = 'https://{0}/services/search/duvet.do'.format(dns.rstrip())
    headers = {'app-id': '4894f63625ed4dfc809b11ac42c2ae8b', 'Services-Source-Type': 'SDSS-Web', 'Accept': 'application/json'}
    resp = requests.get(url, verify=False, headers=headers)
    print(resp)
    parsed = json.loads(resp.text)
    #print(type(parsed))
    #print(parsed.keys())
    #print(parsed['messages']['status'])

    resp_text = resp.text
    utf_8_response = resp_text.encode('utf8')

    test = get_all(utf_8_response, 'messages')
    # if you don't encode to a string/utf8 etc it will not parse corectly, since it is unicode
    #test = get_all(resp.text, 'messages')

    sample_json1=[{"globalControlId": 72, "value": 0, "controlId": 2},
                               {"globalControlId": 77, "value": 3, "controlId": 7}]
    sample_json2=[{"globalControlId": 72, "value": 0, "controlId": 2},
                               {"globalControlId": 77, "value": 3, "controlId": 7}]

    print('equals test', sample_json1 == sample_json2)


    string_sample_json1="""[{"globalControlId": 72, "value": 0, "controlId": 2},
                               {"globalControlId": 77, "value": 3, "controlId": 7}]"""
    string_sample_json2="""[{"globalControlId": 72, "value": 0, "controlId": 2},
                               {"globalControlId": 77, "value": 3, "controlId": 7}]"""
    string_sample_json3="""[{"globalControlId": 72,    "value": 0, "controlId": 2},
                               {"globalControlId": 77, "value":    3,     "controlId": 7}]"""

    x = json.loads(string_sample_json1)
    y = json.loads(string_sample_json2)
    z = json.loads(string_sample_json3)

    print('json loads equals example', x == y)
    print('json loads equals example spaces are off', x == z)

    pp = json.dumps(resp.json(), indent=4)
    print(pp)

def get_all(myjson, key):
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

init()


#pretty print
#parsed = json.dumps(resp.json(), indent=4)
#print parsed

