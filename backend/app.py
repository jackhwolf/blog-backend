from flask import Flask, Blueprint, make_response, jsonify
from flask_restplus import Resource, Api, reqparse
import werkzeug
from flask_cors import CORS
from ddb import PostDescAndMetricDDB
import json
import decimal
import time
import os
from uuid import uuid4
from dotenv import load_dotenv

# load token
load_dotenv('.token')
TOKEN = os.environ.get('token')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

#########
# SETUP #
#########

# setup Flask
app = Flask(__name__)
CORS(app)
api_bp = Blueprint('api', __name__, url_prefix='/v1')
api = Api(api_bp)

# setup ddb conn
descMetrDB = PostDescAndMetricDDB()
print(descMetrDB.create())

#######
# API #
#######

def handleret(data, **kw):
    ''' handle our API response '''
    d = json.dumps(data, indent=4, cls=DecimalEncoder)
    return make_response(d, kw.get('code', 200))

def makekey():
    return f"{uuid4().hex}==={int(time.time())}"


@api.route('/blogpost')
class blogpost(Resource):
    '''
    api endpoint for getting/posting files
    '''

    def post(self):
        '''
        post a new blogpost description entry
        @args:
            title: title of post
            desc:  short description of post, clickbait
            tags:  list of tags delimd by ", "
            token: secure token 
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help='Title of post.')
        parser.add_argument('desc', required=True, help='Short description.')
        parser.add_argument('tags', required=True, help='Delimd tags.')
        parser.add_argument('token', required=True,
                            help='secure password', location='headers')
        args = dict(parser.parse_args())
        if args['token'] == TOKEN:
            key = makekey()
            args['postid'] = key
            descMetrDB.putPost(args, **{'author': 'Jack Wolf'})
            return handleret({"uploadkey": key})
        else:
            return handleret({"message": "auth failed"}, code=401)

    def get(self):
        ''' scan table, format entries, and send back'''
        scan = descMetrDB.scanPosts().get('Items', [{}])
        data = []
        for s in scan:
            post = s['post']['M']
            post = {k: v[list(v)[0]] for k, v in post.items()}
            data.append({'postid': s['postid']['S'], 'post': post})
        data = sorted(data, key=lambda x: int(x['postid']), reverse=True)
        return handleret({'data': data})


@api.route('/metrics')
class metrics(Resource):
    ''' how I will report metrics for posts '''

    def post(self):
        '''
        update metrics for a post
        @args:
            postid: ID of post to update
            metric: either "click" or "like"    
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('postid', required=True, help="post ID")
        parser.add_argument('metric', required=True, help="click or like")
        args = parser.parse_args()
        resp = descMetrDB.updateMetrics(
            args['postid'], f"{args.get('metric', 'click')}s"
        )
        return handleret(resp)

@api.route('/test')
class test(Resource):

    def get(self):
        print("[/v1/test] GET")
        return {"test": "success"}


# run it locally
app.register_blueprint(api_bp)
app.run(debug=True)
