# hold patches

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
 
# Flask rest API
from flask_restful import Resource
from flask_restful import abort
 
# marshmallow
from marshmallow import Schema
from marshmallow import fields
from marshmallow import pprint
from marshmallow import ValidationError
 
# setup MetaData catalog
metadata = MetaData()

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


class AllPatches( Resource ):
       def get( self ):
             ret_data = []
             
             conn = engine.connect()
             s = select([patches])
             result = conn.execute(s)
             
             for row in result:
                   ret_data.append( {'id': row[patches.c.id], 
                                     'server': row[patches.c.server], 
                                     'patch': row[patches.c.patch],
                                     'version': row[patches.c.patch_ver],
                                     'app_patch': row[patches.c.application_patch]})
              
             if ret_data:              
                  result.close()
                  return {"allRecords": ret_data }
             else:
                   result.close()
                   abort(404, message="Failed to find any patches in database".format(server_name))

      
class SinglePatch( Resource ):
       def get(self, server_name):
             
             tst_data = {'server_name': server_name }
             ret_data = []
             
             # verify vaild data has been inputted
             rsp = SingleServerSchema().load( tst_data )
             if rsp[1]:
                  return {"Invalid": rsp[1] }
                  
             s = select([patches.c.id, 
                                    patches.c.server,
                                    patches.c.patch,
                                    patches.c.patch_ver,
                                    patches.c.application_patch]).where(patches.c.server == server_name )
                                    
             conn = engine.connect()
             
             for row in conn.execute(s):
                    ret_data.append({"patch_id": row[patches.c.id], 
                                     "user_id": row[patches.c.server], 
                                     "patch": row[patches.c.patch],
                                     "version": row[patches.c.patch_ver],
                                     "app_patch": row[patches.c.application_patch]} )
             
             if ret_data:
                   return {"SingleRec": ret_data }
             else:
                   abort(404, message="Failed to find any patches in database for server {}".format(server_name))  

                          
       def post( self, server_name):
             ''' Inserts a new record into the database '''
             conn = engine.connect()
             
             try:             
                  ins = patches.insert()
                  result = conn.execute(ins, 
                                        server=request.form['ser'],
                                        patch=request.form['pat'],
                                        patch_ver= request.form['ver'],
                                        application_patch= request.form['app'],
                                       )
             except StatementError  as e:
                   result.close()
                   return {"Error": "Insert of Record failed", "SQLAlError": e }
                   
             result.close()
             return {"inserted": request.form['ser'], "patch": request.form['pat'] }
       
