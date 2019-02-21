import json

from flask_restful import abort
from flask_restful import Resource
from flask_restful import reqparse

from DeviceVal import ContractSchema
from DeviceVal import DeviceMonSchema
from DeviceVal import DeviceDateSchema 

import DataBase

class Device(Resource):
    def get(self, contract_num ):
       ''' returns information on single record '''

       # verify valid input contract number, pass in dict 
       tst_input = {'contract': contract_num }
       rsp = ContractSchema().load(tst_input)
       if not rsp[0]:
          return {'Invalid Contract Number:': rsp[1]['contract']}

       # setup sqlalchemy here
       rsp = DataBase.get_data_by_contract(contract_num)
       return {'response': rsp}

class Devices(Resource):
    def get(self ):
      ''' returns information on a local or remote ip address '''

      # parse the input data 
      parse = reqparse.RequestParser()
      parse.add_argument('month', type=str, help='by month only')
      parse.add_argument('date', type=str, help='by date only')
      args = parse.parse_args()

      # validate input data
      rsp = DeviceMonSchema().load({'month':args['month']})
      if rsp[1]:
         return {'Invalid month': rsp[1]['month']}
       
      rsp = DeviceDateSchema().load({'date':args['date']})
      if rsp[1]:
         return {'Invalid date:': rsp[1]['date']}

      #   setup the select, sqlalchemy
      if args['month'] and args['date']:
         find_by = args['month'] + args['date']
      elif args['month']:
         find_by = args['month']
      elif args['date']:
         find_by = args['date']

      return {'nameis': find_by}


class AllDevices(Resource):
  def get(self):
      return {'nameall': 'allstuff'}

