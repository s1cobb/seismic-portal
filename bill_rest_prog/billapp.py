#!/usr/bin/python

from flask import Flask
from flask_restful import Api

# user defined classes
from Resources.Devices import Device
from Resources.Devices import Devices
from Resources.Devices import AllDevices

from Resources.Conferences import Conference
from Resources.Conferences import Conferences
from Resources.Conferences import AllConferences

# setup app
app = Flask(__name__)
api = Api(app)

# all routes here
api.add_resource(Device, '/api/device/<string:contract_num>')
api.add_resource(Devices, '/api/devices')
api.add_resource(AllDevices, '/api/alldevices')

api.add_resource(Conference,'/api/conference/<string:name>')
api.add_resource(Conferences,'/api/conferences')
api.add_resource(AllConferences, '/api/allconference')


if __name__ == '__main__':
   app.run( debug=True, port=5010)

