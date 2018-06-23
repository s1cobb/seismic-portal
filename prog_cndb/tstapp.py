
# hold app and routes
 
#  Test mockup for upcoming project. 
#  Will use sqlite for testing only.

#  Flask, sqlite, flask-restful, sqlalchemy, marshmallow

# r = requests.post('http://127.0.0.1:5000/api/server/add', 
#                    data = { 'ser': 'NPOWRTPVWSVCAS1', 
#                             'type': 'certificate', 
#                             'os': 'windows', 
#                             'ver': '2012', 
#                             'pat':'y', 
#                             'dat': '05/29/2018', 
#                             'ip': '192.168.132.111', 
#                             'net': 'boxcar'})


# r = requests.post('http://127.0.0.1:5000/api/patches/add', 
#                    data = { 'ser': 'NPOWRTPVWSVCAS1', 
#                             'pat': '0R22J44X', 
#                             'ver':'1.0', 
#                             'app': 'kernel'})
# Flask rest API
from flask import Flask
from flask_restful import Api
from flask_restful import abort
from flask_restful import reqparse
from flask_restful import Resource

from resources.Servers   import AllServers
from resources.Servers   import SingleServer
from resources.Patch     import AllPatches
from resources.Patch     import SinglePatch
from resources.ServerPatches import ServerPatches

# setup flask and flask restful objects
app = Flask(__name__)
api = Api(app)

###################################################
api.add_resource(AllServers,   '/api/servers' )
api.add_resource(SingleServer, '/api/server/<string:server_name>' )
api.add_resource(AllPatches,   '/api/patches')
api.add_resource(SinglePatch,  '/api/patches/<string:server_name>')
api.add_resource(ServerPatches,'/api/patches/alldata')

if __name__ == '__main__':
      app.run( debug=True)

