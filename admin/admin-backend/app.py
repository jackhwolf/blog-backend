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
base_repo = 'https://github.com/jackhwolf/blog/raw/master/src/posts/{}'
post_base_dir = base_dir + '/src/posts/{}'

# setup app
app = Flask(__name__)
CORS(app)


#########
# LOGIC #
#########

def fixMediaPaths(filepath, postid, mpaths):
    '''
    If there are media files referenced in the markdown file
    we need to rename the links in the file to point to the 
    media files new url in the git repo
    @args:
        filepath: str, path to markdown file on local
        postid:   str, unique id of post. used to form url
        mpaths:   list of str, local paths to media files
    @return None
    '''
    with open(filepath, 'r') as fp:
        contents = fp.read()
        for mp in mpaths:
            mp = mp.split('/')[-1]
            contents = contents.replace(mp, base_repo.format(postid) + "/" + mp)
    with open(filepath, 'w') as fp:
        fp.write(contents)
    return None

def redeploy(json):
    '''
    Take our local markdown (and maybe media files) and move them to 
    local git repo for /blog, then call some commands to push changes
    and redeploy to GitHub-pages
    If an error is thrown, it is caught and returned as part of response
    @args:
        json: dict, data from request
    @return: None
    '''
    ddst = post_base_dir.format(json['postid'])
    os.makedirs(ddst, exist_ok=True)
    dst = f"{ddst}/post.md"
    shutil.copy(json['localbase'] + json['localpath'], dst)
    mpaths = json['mediapaths']
    if mpaths != '':
        mpaths = mpaths.split(', ')
        fixMediaPaths(dst, json['postid'], mpaths)
        for mp in mpaths:
            shutil.copy(json['localbase'] + mp, ddst + "/" + mp.split('/')[-1])
    owd = os.getcwd()
    os.chdir(base_dir)
    os.system("git add src/posts/*; git commit -m \"submission: [$(date)]\"; git push -u origin master; npm run deploy")
    os.chdir(owd)
    return None


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
