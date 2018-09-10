# holds classes for servers

from sqlalchemy.sql import or_
from sqlalchemy.sql import and_
from sqlalchemy.sql import not_
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Sequence
from sqlalchemy.sql import select
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine

from sqlalchemy.exc import DBAPIError
from sqlalchemy.exc import StatementError
from sqlalchemy.exc import SQLAlchemyError
 
# Flask rest API
from flask import request
from flask_restful import Resource
from flask_restful import abort
 
# marshmallow
from marshmallow import Schema
from marshmallow import fields
from marshmallow import pprint
from marshmallow import ValidationError
 
# setup MetaData catalog
metadata = MetaData()

# Map devices object to SQL Devices table
devices = Table('Devices', metadata,
       Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
       Column('server', String(25)),
       Column('type', String(25)),
       Column('os', String(5)),
       Column('version', String(6)),
       Column('patched', String(10)),
       Column('patched_date', String(25)),
       Column('ip', String(20)),
       Column('network', String(10)),
)

# creates instance of engine, core interface to the database
engine = create_engine('sqlite:///C:\\myscripts\\inventory_db.sqlite')

# if needed, will create the above tables in the sqlite database
# metadata.create_all(engine)

# definition used with marshmallow for validation
def validate_server_nm(n):
       if n.isdigit():
             raise ValidationError('Server name cannot be numeric only')

# marshmallow validation
class SingleServerSchema( Schema ):
    server_name   = fields.Str(validate=validate_server_nm, required=True)


class AllServers( Resource ): 
     def get(self):
       ''' Returns all the current users in the database '''
       ret_data = []
       
       conn = engine.connect()
       s = select( [devices] )
       result = conn.execute(s)
       
       for row in result:
             ret_data.append( {'id': row[devices.c.id], 
                               'server': row[devices.c.server], 
                               'type': row[devices.c.type],
                               'os': row[devices.c.os],
                               'version': row[devices.c.version],
                               'patched': row[devices.c.patched],
                               'patched_date': row[devices.c.patched_date],
                               'ip': row[devices.c.ip],
                               'network': row[devices.c.network],
                              }
                            )

       if ret_data:
             result.close()       
             return {"allRecords": ret_data }
       else:
             result.close()
             abort(404, message="Failed to find any servers in database".format(server_name))
             
                      
class SingleServer( Resource ):
                                                                       
      def get(self, server_name):
             ''' Returns a single user from database '''
             
             tst_data = {'server_name': server_name }
             ret_data = []
             
             # verify vaild data has been inputted
             rsp = SingleServerSchema().load( tst_data )
             if rsp[1]:
                  return {"Invalid": rsp[1] }
             
             conn = engine.connect()
             s = select([devices.c.id, 
                         devices.c.server,
                         devices.c.type,
                         devices.c.os,
                         devices.c.version,
                         devices.c.patched,
                         devices.c.patched_date,
                         devices.c.ip,
                         devices.c.network]).where(devices.c.server == server_name)
             
             for row in conn.execute(s):
                    ret_data.append( {'id': row[devices.c.id], 
                                      'server': row[devices.c.server], 
                                      'type': row[devices.c.type],
                                      'os': row[devices.c.os],
                                      'version': row[devices.c.version],
                                      'patched': row[devices.c.patched],
                                      'patched_date': row[devices.c.patched_date],
                                      'ip': row[devices.c.ip],
                                      'network': row[devices.c.network]}
                                   )
                    
             if ret_data:       
                    return {"ServerData": ret_data }
             else:
                   abort(404, message="Id {} does not exist in database".format(server_name))
      
      def post( self, server_name):
             ''' Inserts a new record into the database '''
             
             tst_data = {'server_name': request.form['ser']}
             
             # verify vaild data has been inputted
             rsp = SingleServerSchema().load( tst_data )
             if rsp[1]:
                  return {"Invalid": rsp[1] }
             
             conn = engine.connect()
             
             try:             
                  ins = devices.insert()
                  result = conn.execute(ins, 
                                        server=request.form['ser'],
                                        type=request.form['type'],
                                        os=request.form['os'],
                                        version= request.form['ver'],
                                        patched= request.form['pat'],
                                        patched_date = request.form['dat'],
                                        ip = request.form['ip'],
                                        network = request.form['net'] )
             except StatementError  as e:
                   result.close()
                   return {"Error": "Insert of Record failed", "SQLAlError": e }
                   
             result.close()
             return {"inserted": request.form['ser'] }
                   
      def put(self, server_name):
             row = {}
             
             tst_data = {'server_name': server_name }
             
             # verify vaild data has been inputted
             rsp = SingleServerSchema().load( tst_data )
             if rsp[1]:
                  return {"Invalid": rsp[1] }
                  
             conn = engine.connect()
             
             # verify we actually have a record to update
             s = select([devices.c.server]).where(devices.c.server == server_name )
             rsp = conn.execute(s)
             row = rsp.fetchone()
             if not row:
                   abort(404, message =  "Server {} does not exist in database".format(server_name))
             
             # update record             
             try:
                   stmt = devices.update().where(devices.c.server == server_name).values(patched = request.form['pat'])
                   result = conn.execute(stmt)
             except StatementError as e:
                   result.close()
                   return {"Error": "update not completed", "ErrMsg": e }
             
             result.close()             
             return {"updated server_name": request.form['ser'], "patched": request.form['pat']} 
            
      def delete(self, server_name):
            pass
