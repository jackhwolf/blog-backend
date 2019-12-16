from flask import Flask, make_response
from flask_restplus import Api, Resource, reqparse
import json      # to format API responses
import time
from userlocalstorage import UserLocalStorage

'''
create app object
__name__ tells the object to look for resources in this modules path
'''
app = Flask(__name__)
api = Api(app)

''' setup local storage '''
users = UserLocalStorage()

''' setup request parser to parse data out of requests '''
parser = reqparse.RequestParser()
parser.add_argument('uname', type=str, required=True, help='Username of specified user.')
for arg, hlp in [['email', 'users email'], 
                 ['location', 'users location'],
                 ['favoriteFood', 'users favorite food'],
                 ['attrs', 'comma-separated string of attributes']]:
    parser.add_argument(arg, type=str, help=hlp)

'''define routes '''
@api.route('/test')
class test(Resource):
    ''' test route '''

    def get(self):
        return make_response(json.dumps({'response': f'success @ {int(time.time())}'}))

@api.route('/user')
@api.expect(parser)  # this gives our class/methods access to our predefined req_parser
class user(Resource):
    ''' route to get/post/delete user info '''

    def get(self):
        args = parser.parse_args()
        uname = args.pop('uname')
        resp = users.get(uname, args)
        return make_response(json.dumps({'response': str(resp)}))

    def post(self):
        args = parser.parse_args()
        uname = args.pop('uname')
        resp = users.add(uname, args)
        return make_response(json.dumps({'response': str(resp)}))

    def patch(self):
        args = parser.parse_args()
        uname = args.pop('uname')
        resp = users.update(uname, args)
        return make_response(json.dumps({'response': str(resp)}))

    def delete(self):
        args = parser.parse_args()
        uname = args.pop('uname')
        resp = users.delete(uname, args)
        return make_response(json.dumps({'response': str(resp)}))

'''run app locally''' 
app.run(port=8000, debug=True)
