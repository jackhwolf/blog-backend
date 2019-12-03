import requests
import json

class sender:
    ''' class to help send requests to api '''

    def __init__(self, url):
        ''' 
        store url to ping, map of `requests` methods,
        and dict for results
        '''
        self.url = url.rstrip('/')
        self.mmap = {
            'get': requests.get,
            'post': requests.post
        }
        self.results = {}
    
    def send(self, method, params='/'):
        '''
        send a request of HTTP type method to self.url+params
        appends result to self.results[method]
        @args:
            method: str, HTTP method to send. Currently supported: GET, POST
            params: str, route params, defaults to root
        @return:
            json response from server
        '''
        func = self.mmap[method]
        rlist = self.results.get(method, [])
        result = func(self.url + params).json()
        rlist.append([method, params, result])
        self.results[method] = rlist
        return result

    def showresults(self):
        ''' iterate thru and print off results '''
        for key in self.results:
            print(key)
            for res in self.results[key]:
                for i, k in enumerate(['method', 'params', 'response']):
                    print(f"\t{k}: {res[i]}")
                print('\n')

