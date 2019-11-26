import boto3
from boto3.dynamodb.conditions import Key, Attr, Not
import time
from uuid import uuid4
import os
from dotenv import load_dotenv


# load in keys
load_dotenv()


#################
# base db class #
#################

class db:
    ''' i throw errors '''

    def __init__(self):
        self.res = boto3.resource(
                'dynamodb',
                aws_access_key_id=os.environ.get('awsaccess'),
                aws_secret_access_key=os.environ.get('awssecret'),
                region_name='us-west-1'
            )

    def getcli(self):
        ''' get a client '''
        return boto3.client(
                        'dynamodb',
                        aws_access_key_id=os.environ.get('awsaccess'),
                        aws_secret_access_key=os.environ.get('awssecret'),
                        region_name='us-west-1'
                    )

    def create__(self, tid, schema, atr_defn, **kw):
        ''' attempt to create this db table '''
        self.res.create_table(
            TableName=tid,
            KeySchema=schema,
            AttributeDefinitions=atr_defn,
            ProvisionedThroughput={
                "ReadCapacityUnits": kw.get('RCU', 2),
                "WriteCapacityUnits": kw.get('WCU', 2)
            }
        )
        return 1

    def put_(self, table, item, **kw):
        ''' attempt to put an item into table '''
        if not issubclass(type(item), list):
            item = [item]
        for i in item:
            table.put_item(Item=i)
        return 1

    def get_(self, table, query, **kw):
        ''' attempt to get an item into ddb '''
        resp = table.query(KeyConditionExpression=query)
        return resp

    def update_(self, table, updatestmt, **kw):
        ''' attempt to update an item into ddb '''
        return -1

    def delete_(self, table, query, **kw):
        ''' attempt to delete an item into ddb '''
        resp = table.delete_item(**query)
        return resp

    def scan_(self, tid, **kw):
        ''' scan the table '''
        cli = self.getcli()
        return cli.scan(TableName=tid, **kw)



##################
# super db class #
##################

class superdb(db):
    ''' i handle errors '''

    def __init__(self, tid, ks, atr_defn):
        ''' store this table and tableID '''
        db.__init__(self)
        self.tid = tid
        self.table = self.res.Table(tid)

    def create_(self, *args, **kw):
        ''' create our db table '''
        try:
            return True, self.create__(*args, **kw)
        except Exception as e:
            return False, str(e)

    def put(self, item, **kw):
        ''' put something or report error '''
        try:
            return True, self.put_(self.table, item, **kw)
        except Exception as e:
            return False, str(e)

    def get(self, query, **kw):
        ''' get something or report error '''
        try:
            return True, self.get_(self.table, query, **kw)
        except Exception as e:
            return False, str(e)

    def update(self, updatestmt, **kw):
        ''' update something or report error '''
        try:
            return True, self.update_(self.table, updatestmt, **kw)
        except Exception as e:
            return False, str(e)

    def delete(self, query, **kw):
        ''' delete something or report error '''
        try:
            return True, self.delete_(self.table, query, **kw)
        except Exception as e:
            return False, str(e)


##################
# post-ddb class #
##################

class postddb(superdb):
    ''' i work with the post ddb table '''

    def __init__(self, **kw):
        ''' store info abt table '''
        self.tid = 'mywebsite-posts'    # name of table
        self.ks = [                        # schema for keys
                    {
                        'AttributeName': 'postid',
                        'KeyType': 'HASH'
                    }
                ]
        self.atr_defn = [                  # what types are our keys
                    {
                        'AttributeName': 'postid',
                        'AttributeType': 'S'
                    }
                ]
        superdb.__init__(self, self.tid, self.ks, self.atr_defn)

    def create(self):
        ''' create me '''
        return self.create_(self.tid, self.ks, self.atr_defn)

    def fmtentry__(self, e, **kw):
        ''' make sure ddb entry is standard '''
        e = {
            'postid': e['postid'],
            'post': {
                'author': e.get('author', kw.get('author', 'Jack Wolf')),
                'title':   e.get('title', '-'),
                'desc': e.get('desc', '-'),
                'tags':    e.get('tags', '-'),
            },
            'metrics': {
                'clicks': 0,
                'favs':   0
            },
        }
        return e

    def putPost(self, post, **kw):
        ''' put a post into our ddb '''
        return self.put(self.fmtentry__(post), **kw)

    def getPost(self, postid, **kw):
        ''' get a post from our ddb '''
        query = Key('postid').eq(postid)
        flag, data = self.get(query, **kw)
        if flag:
            data = data.get('Items', [{}])[0]
        return flag, data

    def scanPosts(self, **kw):
        return self.scan_(self.tid)

    def updatePost(self, updatestmt, **kw):
        ''' update a post in our ddb '''
        return self.update(updatestmt, **kw)

    def deletePost(self, postid, **kw):
        ''' delete a post from our ddb '''
        dkw = {
            'Key': {
                'postid': postid
            },
            'ConditionExpression': "postid = :val",
            'ExpressionAttributeValues': {
                ":val": postid
            }
        }
        return self.delete(dkw, **kw)

    def updateMetrics(self, postid, metric, **kw):
        ''' update the metrics of some post '''
        pass
