from flask import Flask 
import time

# create app object
# __name__ tells the object to look for resources
#  in this modules path
app = Flask(__name__)


################# 
# define routes #
#################

@app.route('/test')
def test():
    '''
    a simple route which by default only accepts GET requests
    we can use this to make sure our server is running
    '''
    return {'status': 'success', 'time': str(int(time.time()))}

# run app
app.run(port=8000, debug=True)

