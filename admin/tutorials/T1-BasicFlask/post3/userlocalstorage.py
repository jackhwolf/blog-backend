import time 
import json


''' class to store each user '''
class User:

    def __init__(self, name, kw):
        self.info =  {
            'userInfo': {
                'name': name,
                'signupTime': str(int(time.time())),
            },
            'userData': {
                'email': kw.get('email', ''),
                'location': kw.get('location', ''),
                'favoriteFood': kw.get('favoriteFood', '')
            }
        }

''' class to store users locally '''
class UserLocalStorage:

    def __init__(self):
        self.users = {}

    def add(self, uname, data):
        ''' 
        add uname to users if not already there 
        @args:
            data: dict, dictionary of user information
        '''
        if self.users.get(uname) is None:
            self.users[uname] = User(uname, data).info
            return True
        return False

    def update(self, uname, data):
        '''
        update an existing entry
        @args:
            uname: str,  username of user
            data:  dict, dictionary of k-v pairs
        @return
            True on success, False on failure or if user doesn't exist
        '''
        user = self.users.get(uname)
        if user is not None:
            if data['attrs'] is not None:
                attrs = data['attrs']
                for k in attrs:
                    if k in user['userData']:
                        user['userData'][k] = attrs[k]
            return user
        return False

    def get(self, uname, data):
        ''' check if uname is in users '''
        user = self.users.get(uname)
        if user is not None:
            user = user
            if data['attrs'] is not None:
                ud = {a: user['userData'].get(a) for a in data['attrs'].split('&')}
                user['userData'] = ud
        return user

    def delete(self, uname, data):
        ''' delete user if they are present '''
        if uname in self.users:
            if data['attrs'] is not None:
                user = self.users.get(uname)
                [user['userData'].pop(a, None) for a in data['attrs'].split('&')]
            else:
                del self.users[uname]
            return True
        return False



