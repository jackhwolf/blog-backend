from flask import Flask, Blueprint, make_response, jsonify
from flask_restplus import Resource, Api, reqparse
import werkzeug
from flask_cors import CORS
from ddb import postddb
import json
import decimal
import time
import os

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
pdb = postddb()
print(pdb.create())

#######
# API #
#######

def handleret(data, **kw):
    ''' handle our API response '''
    d = json.dumps(data, indent=4, cls=DecimalEncoder)
    return make_response(d, kw.get('code', 200))

'''
procedure to post a file:
    1) send POST request to /blogpost/create with relevant data
        - request:  title:    title of post
                    desc:     short desc of post to display
                    tags:     delim'd string of tags
        - response: postid:   id of post
       use BlogpostMap to map id to filename until files posted
    2) send PUT request to /blogpost/upload with relevant files
        - request:  key:      post id from /submit/post response
                    file:     file object
                    filetype: markdown or media
        - response: 0 on fail, 1 on success
'''

class BlogpostMap:
    '''
    we give user a key to make a blogpost file object
    we have to check key and map it to filename
    '''

    def __init__(self):
        ''' maintain refs to posts and our data '''
        self.base_dirname = '../frontend/src/posts/{}'
        self.data = {}

    @property
    def n(self):
        ''' how many are we tracking '''
        return len(self.data.keys())

    def add(self):
        ''' add a new file object to be created '''
        k = str(int(time.time()*1000))
        self.data[k] = self.base_dirname.format(k)
        return k

    def get(self, k):
        ''' get base_dirname of file object w/ given key '''
        return self.data.get(k, -1)

    def delete(self, k):
        ''' done uploading files to key '''
        _ = self.data[k]
        del self.data[k]
        return _

bmap = BlogpostMap()

@api.route('/blogpost/create')
class submitmedia(Resource):
    ''' how I will get ready to submit a posts files '''

    def post(self):
        ''' take a file and write to media directory '''
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True, help='Title of post.')
        parser.add_argument('desc', required=True, help='Short description.')
        parser.add_argument('tags', required=True, help='Delimd tags.')
        args = dict(parser.parse_args())
        postobjkey = bmap.add()
        args['postid'] = postobjkey
        pdb.putPost(args, **{'author': 'Jack Wolf'})
        return handleret({"uploadkey": postobjkey})

@api.route('/blogpost/upload')
class submitmedia(Resource):
    ''' how I will submit markdown and media files assoc. w/ a post '''

    def put(self):
        ''' take a file and write to media directory '''
        parser = reqparse.RequestParser()
        parser.add_argument('postid', required=True, help='Unique id of post.')
        parser.add_argument('filetype', required=True, help='markdown or media.')
        parser.add_argument('content', required=True, help='content of file.')
        # only for images
        parser.add_argument('filename', default="mediafile.ext")
        parser.add_argument('mode')
        parser.add_argument('size1')
        parser.add_argument('size2')
        args = parser.parse_args()
        dirname = bmap.get(args['postid'])
        ftype = args.get('filetype')
        if ftype.lower() == 'media':
            ftype = "media"
            fname = args.get('filename', 'media')
        else:
            ftype = "markdown"
            fname = "post.md"
        dirname = f"{dirname}/{ftype}"
        os.makedirs(dirname, exist_ok=True)
        fname = f"{dirname}/{fname}"
        if ftype == 'markdown':
            with open(fname, "wb") as f:
                f.write(args['content'].encode('utf-8'))
        return {"filename": fname}

@api.route('/blogpost/getposts')
class paginate(Resource):
    ''' how we send blogpost cards - for now just sending all '''

    def get(self):
        ''' scan table, format, and send '''
        scan = pdb.scanPosts().get('Items', [{}])
        data = []
        for s in scan[:10]:
            post = s['post']['M']
            post = {k: v[list(v)[0]] for k,v in post.items()}
            data.append({'postid': s['postid']['S'], 'post': post})
        data = sorted(data, key=lambda x: int(x['postid']))
        return handleret({'data': data})


@api.route('/metrics')
class metrics(Resource):
    ''' how I will report metrics for posts '''

    def post(self):
        ''' update metrics for a post '''
        parser = reqparse.RequestParser()
        parser.add_argument('postid')
        parser.add_argument('metric')
        args = parser.parseargs()
        resp = pdb.updateMetrics(args['postid'], args.get('metric', 'clicks'))
        return handleret(resp, skey='UpdateResults')


# run it locally
app.register_blueprint(api_bp)
app.run(debug=True)
