from flask import Flask, request  # request library to get request info
import json      # to format API responses
import time

'''
create app object
__name__ tells the object to look for resources in this modules path
'''
app = Flask(__name__)

''' set to store users '''
users = set()


'''define routes '''

@app.route('/test')
def test():
    '''
    a simple route which by default only accepts GET requests
    we can use this to make sure our server is running
    '''
    return {'status': 'success', 'time': str(int(time.time()))}


@app.route('/user/<string:name>', methods=['GET', 'POST'])
def user(name):
    '''
    this route accepts two methods and one url parameter
    if GET:
        return True if name exists in users, False otherwise
    if POST:
        return False if name exists in users, else add to 
        usera and return True
    '''
    if request.method == 'GET':
        return json.dumps({'response': str(name in users)})
    elif request.method == 'POST':
        if name in users:
            return json.dumps({'response': str(False)})
        users.add(name)
        return json.dumps({'response': str(True)})
    else:
        return json.dumps({'response': 'method not allowed'})


'''run app locally'''
app.run(port=8000, debug=True)
