import pymysql
from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

######
#  testing 1
# i will be testing again

class Message(Resource):
    ''' Rest API interface to the MySql message database for
        maintaining messages received from rabbitmq 
    ''' 
    def __init__(self):
       self.host = 'localhost'
       self.user = 'root'
       self.passwd = 'steve'
       self.db = 'messages'
       
    def get(self, id):
       ''' Fetch all records from database matching the id '''
       conn = pymysql.connect(host = self.host, 
                            user = self.user, 
                            passwd = self.passwd, 
                            db = self.db,
                            cursorclass=pymysql.cursors.DictCursor)
       
       try:
           with conn.cursor() as cur:
             cur.execute('select * from messages where id = %s', id)
             result = cur.fetchall()
             print(result)
             return jsonify({'message': result})
       except pymysql.err.DataError as e:
           result = "MySQL data error: %s" % e
       except pymysql.err.IntegrityError as e:
           result = "MySQL integrity error: %s" % e
       except pymysql.err.NotSupportedError as e:
           result = "MySQL command not supported %s" % e
       except pymysql.err.OperationalError as e:
           result = "MySQL operation error: %s" % e
       finally:
           conn.close()
       return jsonify({'Error': result})
       
    ##################################################################
    def delete(self, id):
       ''' remove record from MySql database messages '''
       result = 'na'
       conn = pymysql.connect(host = self.host, 
                            user = self.user, 
                            passwd = self.passwd, 
                            db = self.db,
                            cursorclass=pymysql.cursors.DictCursor)
       
       sql = 'delete from messages where id = %s' % id
       print(sql)
       try:
           with conn.cursor() as cur:
             cur.execute(sql)
             conn.commit()
             recr = cur.rowcount  
             if recr != 0:
                 print("Number of rows affected: %d" % recr)
                 result = {'numofrecs':recr}
       except pymysql.err.DataError as e:
           result = "MySQL data error: %s" % e
       except pymysql.err.IntegrityError as e:
           result = "MySQL integrity error: %s" % e
       except pymysql.err.NotSupportedError as e:
           result = "MySQL command not supported %s" % e
       except pymysql.err.OperationalError as e:
           result = "MySQL operation error: %s" % e
       finally:
           conn.close()
       return jsonify({'message': result})
       
    #################################################################
    def put(self, id):
       ''' Update records in MySql database messages '''
       conn = pymysql.connect(host = self.host, 
                            user = self.user, 
                            passwd = self.passwd, 
                            db = self.db,
                            cursorclass=pymysql.cursors.DictCursor)
       
       # grab data from http request
       key = request.form['route']
       mesg = request.form['message']
       
       sql = "update messages set route_key = '%s'," \
             "message = '%s' where id = %s" % (key, mesg, id)
       try:
           with conn.cursor() as cur:
             cur.execute(sql)
             conn.commit()
             recr = cur.rowcount
             if recr != 0:
                 print("Number of rows affected: %d" % recr)
                 result = {'numofrecs':recr}
             else:
                 print("ERROR: message table was not updated")
                 result = {'numofrecs':0}
       except pymysql.err.DataError as e:
           result = "MySQL data error: %s" % e
       except pymysql.err.IntegrityError as e:
           result = "MySQL integrity error: %s" % e
       except pymysql.err.NotSupportedError as e:
           result = "MySQL command not supported %s" % e
       except pymysql.err.OperationalError as e:
           result = "MySQL operation error: %s" % e
       finally:
           conn.close()
       return jsonify({'message': result})
       
       
    #################################################################
    # testing with requests:
    # requests.post('http://127.0.0.1/id/6', \
    #          data={"route":value1, "message":msg}).json()   
    def post(self, id):
       ''' Insert records in MySql database messages from rabbitmq '''
       conn = pymysql.connect(host = self.host, 
                            user = self.user, 
                            passwd = self.passwd, 
                            db = self.db,
                            cursorclass=pymysql.cursors.DictCursor)
       
       key_value = request.form['route']
       message   = request.form['message']
       
       sql = "insert into messages (id, route_key, message) " \
             "values (%s, '%s', '%s')" % (id, key_value, message)

       try:
           with conn.cursor() as cur:
             cur.execute(sql)
             conn.commit()
             recr = cur.rowcount
             print("recr: %s" % recr)
             if not recr:
                 result = {'numofrecs':recr}
             else:
                 result = {'numofrecs':0}
       except pymysql.err.DataError as e:
           result = "MySQL data error: %s" % e
           print("MySQL data error: %s" % e)
       except pymysql.err.IntegrityError as e:
           result = "MySQL integrity error: %s" % e
           print("MySQL integrity error: %s" % e)
       except pymysql.err.NotSupportedError as e:
           result = "MySQL command not supported %s" % e
           print("MySQL command not supported: %s" % e)
       except pymysql.err.OperationalError as e:
           result = "MySQL operation error: %s" % e
           print("MySQL operation error: %s" % e)
       finally:
           conn.close()
       return jsonify({'message': result})

#####################################################################       
api.add_resource(Message, '/id/<string:id>')  
    
if __name__ == '__main__':
  app.run(debug = True)
