# server and patches

# sqlalchemy modules
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
 
# Map patches object to SQL patches table
patches = Table('patches', metadata,
       Column('id', Integer, primary_key=True),
       Column('server',  String(25)),
       Column('patch', String(30)),
       Column('patch_ver', String(30)),
       Column('application_patch', String(30)),
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

class ServerPatches( Resource ):
      def get( self ):
             ret_data = []             
             conn = engine.connect()
             
             s = select([devices.c.id, devices.c.server,
                         devices.c.os, devices.c.network,
                         devices.c.patched, patches.c.server,
                         patches.c.patch, patches.c.patch_ver,
                         patches.c.application_patch]). \
                         where( 
                               and_(
                                   devices.c.server == patches.c.server, devices.c.patched == 'y',
                                   )
                              )
             
             for row in conn.execute(s):
                    ret_data.append({"device_id": row[devices.c.id],
                                     "dserver": row[devices.c.server],
                                     "pserver": row[patches.c.server],
                                     "os": row[devices.c.os],
                                     "patched": row[devices.c.patched],
                                     "network": row[devices.c.network],
                                     "patch": row[patches.c.patch], 
                                     "version": row[patches.c.patch_ver], 
                                     "app": row[patches.c.application_patch]} )
             
             if ret_data:
                  return {"AllRecords": ret_data }
             else:
                  abort(404, message="Failed to get the server and patches infomation")
                   
