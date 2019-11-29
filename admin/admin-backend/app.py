from flask import Flask, request, make_response
import os
import shutil
import json
from flask_cors import CORS
import time
import os
from dotenv import load_dotenv

# load in token
load_dotenv('../../backend/.token')
TOKEN = os.environ.get('token')

# setup app
app = Flask(__name__)
CORS(app)

# format response
def handleret(data, **kw):
    ''' handle our API response '''
    d = json.dumps(data, indent=4)
    return make_response(d, kw.get('code', 200))

# where I want to move files
post_base_dir = '/home/twilight/jackhwolf.github.io/githubio/src/posts/{}'


##############
# API routes #
##############

@app.route('/v1/movepost', methods=['POST'])
def movepost():
    ''' move a post from wherever I write them to my blog repo '''
    json = request.json
    if request.headers.get('token') == TOKEN:
        try:
            json = request.json
            dst = post_base_dir.format(json['postid'])
            os.makedirs(dst, exist_ok=True)
            dst = f"{dst}/post.md"
            shutil.move(json['localpath'], dst)
            return handleret({"status": "success"})
        except Exception as e:
            return handleret({"status": "failure", "message": str(e)}, code=500)
    return 


@app.route('/test')
def test():
    ''' check that server is up '''
    return handleret({"test": f"success. {int(time.time())}"})

# run locally
app.run(debug=True)

