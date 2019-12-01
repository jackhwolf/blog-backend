from flask import Flask, request, make_response
import os
import shutil
import json
from flask_cors import CORS
import time
import os
import subprocess as subp
from dotenv import load_dotenv


#########
# SETUP #
#########

# load in token
load_dotenv('../../backend/.token')
TOKEN = os.environ.get('token')

# where I want to move files
base_dir = '/home/twilight/py/mywebsite/frontend'
post_base_dir = base_dir + '/src/posts/{}'

# setup app
app = Flask(__name__)
CORS(app)


#########
# LOGIC #
#########

def redeploy(json):
    dst = post_base_dir.format(json['postid'])
    os.makedirs(dst, exist_ok=True)
    dst = f"{dst}/post.md"
    shutil.move(json['localpath'], dst)
    owd = os.getcwd()
    os.chdir(base_dir)
    os.system(
        "git add src/posts/*; git commit -m \"submission [%(date)]\"; git push -u origin master; npm run deploy")
    os.chdir(owd)
    return True


#############
# API STUFF #
#############

# format response
def handleret(data, **kw):
    ''' handle our API response '''
    d = json.dumps(data, indent=4)
    return make_response(d, kw.get('code', 200))


##############
# API routes #
##############

@app.route('/v1/submitpost', methods=['POST'])
def movepost():
    ''' move a post from wherever I write them to my blog repo '''
    json = request.json
    if request.headers.get('token') == TOKEN:
        try:
            json = request.json
            redeploy(json)
            return handleret({"status": "success"})
        except Exception as e:
            return handleret({"status": "failure", "message": str(e)}, code=500)
    return handleret({"status": "unauthorized"}, code=401)


@app.route('/test')
def test():
    ''' check that server is up '''
    return handleret({"test": f"success. {int(time.time())}"})


# run locally
app.run(debug=True)
