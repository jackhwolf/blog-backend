from flask import Flask, request, make_response
import json      # to format API responses
import time

# create app object
# __name__ tells the object to look for resources in this modules path
app = Flask(__name__)

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
        if self.users.get(uname) == None:
            self.users[uname] = data
            return True
        return False

    def get(self, uname):
        ''' check if uname is in users '''
        return self.users.get(uname, {})

    def delete(self, uname):
        ''' delete user if they are present '''
        if uname in self.users:
            del self.users[uname]
            return True
        return False


users = UserLocalStorage()


'''define routes '''

@app.route('/test')
def test():
    '''
    a simple route which by default only accepts GET requests
    we can use this to make sure our server is running
    '''
    return {'status': 'success', 'time': str(int(time.time()))}


@app.route('/user/<string:uname>', methods=['GET', 'POST', 'DELETE'])
def user(uname):
    '''
    this route accepts two methods and one url parameter
    if GET:
        return True if name exists in users, False otherwise
    if POST:
        return False if name exists in users, else add to 
        usera and return True
    '''
    if request.method == 'GET':
        return make_response(json.dumps({'response': str(users.get(uname))}))
    elif request.method == 'POST':
        data = request.get_json(force=True)
        return make_response(json.dumps({'response': str(users.add(uname, data))}))
    elif request.method == 'DELETE':
        return make_response(json.dumps({'response': str(users.delete(uname))}))
    else:
        return make_response(json.dumps({'response': 'method not allowed'}))


'''run app locally'''
app.run(port=8000, debug=True)
