from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine

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
        query = conn.execute("SELECT * FROM churches WHERE wikidata = '%s'"%wikidata)

        return {'church': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(Church, '/churches/<string:wikidata>')

#TODO actually test this
class BoundingBox(Resource):
    def get(self):
        conn = e.connect()

        args = request.args
        #args['south']
        #args['east']
        #args['north']
        #args['west']

        query = conn.execute("SELECT * FROM churches WHERE lon <= '%(south)s' AND lon >= '%(east)s' AND lat >= '%(north)s' AND lat <= '%(west)s'"%args)

        return {'churches': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(BoundingBox, '/churches/bbox')

class LabelSerach(Resource):
    def get(self):
        conn = e.connect()

        args = request.args
        #args['text']
        text = args['text']

        query = conn.execute("SELECT * FROM churches WHERE label LIKE '%{0}%'".format(text))

        return {'churches': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

api.add_resource(LabelSerach, '/churches/label')

if __name__ == '__main__':
     app.run()