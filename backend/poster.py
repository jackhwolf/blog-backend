import requests
import sys
import time
import json
from PIL import Image
from uuid import uuid4
import os
from dotenv import load_dotenv

# load token
load_dotenv('.token')
TOKEN = os.environ.get('token')

class poster:

    def __init__(self):
        self.url = 'http://127.0.0.1:5000/v1/blogpost'

    def createpost(self, **kw):
        ''' create post obj on server and return key '''
        create = requests.post(
                    self.url,
                    params={
                        'title': kw.get('title'),
                        'desc': kw.get('desc'),
                        'tags': kw.get('tags')
                    },
                    headers={
                        'token': TOKEN
                    })
        return json.loads(create.text)

if __name__ == "__main__":
    p = poster()
    print(p.createpost())

