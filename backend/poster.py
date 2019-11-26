import requests
import sys
import time
import json
from PIL import Image
from uuid import uuid4

class poster:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/v1/blogpost/{}'

    def get_txt_content(self, fp):
        ''' get file content '''
        with open(fp, "rb") as f:
            content = f.read()
        return content

    def get_img_content(self, fp):
        ''' get image content '''
        return self.get_txt_content(fp)

    def createpost(self):
        ''' create post obj on server and return key '''
        create = requests.post(
                    self.url.format('create'),
                    params={
                        'title': str(uuid4()),
                        'desc': str(uuid4()),
                        'tags': 'sample*tags'
                    })
        return json.loads(create.text)['uploadkey']

    def uploadpostfiles(self, key, data):
        ''' upload files assoc w/ post w/ key '''
        upload = requests.put(
                    self.url.format('upload'),
                    params=data)
        return json.loads(upload.text)

    def uploadmd(self, key, fname):
        ''' upload a markdown file '''
        content = self.get_txt_content(fname)
        data = {
            'postid':   key,
            'filetype': 'markdown',
            'content':  content
        }
        return self.uploadpostfiles(key, data)

    def uploadimg(self, key, fname):
        ''' upload an image '''
        content = self.get_img_content(fname)
        data = {
            'postid':   key,
            'filetype': 'media',
            'content':  content,
            'filename': fname.split('/')[-1],
            'mode':     'RBG',
            'size1':    10,
            'size2':    10
        }
        return self.uploadpostfiles(key, data)
