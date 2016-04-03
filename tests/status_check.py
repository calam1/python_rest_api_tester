def check_statuses(response):
    check_response_code(response)
    check_status_message(response)

def check_response_code(response):
    if response.status_code != 200:
        raise ValueError('Response code is not 200, it is:', response.status_code)
    else:
        print('Status is good:', response.status_code)

def check_status_message(response):
    data =  response.json()
    messages = data['messages']
    status_message = messages['status']

    if str(status_message) != 'SUCCESS':
        raise ValueError('Response status message is not successful, response returned was:', status_message)
    else:
        print('Response status message is:', str(status_message))
