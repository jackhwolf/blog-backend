import requests
import json


''' define base url for user routes '''
url = 'http://127.0.0.1:8000/user'


# ''' post and get JACK w/ no data '''
# print(requests.post(url, data={'uname': 'jack'}).text)
# print()
# print(json.dumps(requests.get(url, data={'uname': 'jack',}).json(), indent=4))
# print()


''' post and get SKIPPY w/ data '''
print(requests.post(url, data={
    'uname': 'skippy',
    'email': 'skippy@wolf.com',
    'location': 'San Francisco, CA',
    'favoriteFood': 'peanut butter'
}).text)
print()
print(json.dumps(requests.get(url, data={
    'uname': 'skippy',
    'attrs': 'email&favoriteFood'
}).json(), indent=4))
print()
print(json.dumps(requests.patch(url, data={
    'uname': 'skippy',
    'attrs': {
        'email': 'new@email.com'
    }
}).json(), indent=4))
print()

''' post and get ELVIS w/ data '''
print(requests.post(url, data={
    'uname': 'elvis',
    'email': 'elvis@wolf.com',
    'location': 'San Francisco, CA',
    'favoriteFood': 'cookies'
}).text)
print()
print(json.dumps(requests.get(url, data={
    'uname': 'elvis',
    'attrs': 'favoriteFood&location'
    }).json(), indent=4))
print()

''' delete and get JACK '''
print(json.dumps(requests.delete(url, data={'uname': 'elvis', 'attrs': 'location'}).json(), indent=4))
print()
print(json.dumps(requests.get(url, data={'uname': 'elvis'}).json(), indent=4))
print()