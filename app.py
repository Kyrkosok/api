import sys
from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine

# this is requried for uwsgi web servers/python 2(Tool Labs)
# why sys is reloaded:
# http://www.ianbicking.org/illusive-setdefaultencoding.html
if sys.version[0] == '2':
    reload(sys)
    sys.setdefaultencoding('utf-8')

e = create_engine('sqlite:///database/db.sqlite')

app = Flask(__name__)
api = Api(app)

# CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response

# Returns a list of all churches in the database
# Never use this endpoint
class Churches(Resource):
    def get(self):
        # Connect to databse
        conn = e.connect()
        # Perform query and return JSON data
        query = conn.execute("SELECT * FROM churches")
        return {'churches': [i for i in query.cursor.fetchall()]}

api.add_resource(Churches, '/churches')

class Church(Resource):
    def get(self, wikidata):
        conn = e.connect()
        query = conn.execute("SELECT * FROM churches WHERE wikidata = '{0}'".format(wikidata))

        return {'church': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(Church, '/churches/<string:wikidata>')

class BoundingBox(Resource):
    def get(self):
        conn = e.connect()

        args = request.args
        #args['west']
        #args['east']
        #args['north']
        #args['south']

        query = conn.execute("SELECT `wikidata`, `label`, `lat`, `lon` FROM churches WHERE lon <= {0} AND lon >= {1} AND lat <= {2} AND lat >= {3}".format(float(args['west']), float(args['east']), float(args['north']), float(args['south'])))

        return {'churches': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(BoundingBox, '/churches/bbox')

class LabelSerach(Resource):
    def get(self):
        conn = e.connect()

        args = request.args
        #args['text']
        text = args['text']

        query = conn.execute("SELECT * FROM churches WHERE label LIKE '%{0}%' LIMIT 15".format(text))

        return {'churches': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(LabelSerach, '/churches/label')

class Random(Resource):
    def get(self):
        conn = e.connect()

        args = request.args
        #args['limit']
        limit = args['limit']

        query = conn.execute("SELECT * FROM churches WHERE wikidata IN (SELECT wikidata FROM churches ORDER BY RANDOM() LIMIT {0})".format(limit))

        return {'churches': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(Random, '/churches/random')

if __name__ == '__main__':
    app.run()