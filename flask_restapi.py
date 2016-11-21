import pymysql
from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

class Message(Resource):
    ''' Rest API interface to the MySql message database for
        maintaining messages received from rabbitmq 
    ''' 
        
    def get(self, id):
       ''' Fetch all records from database matching the id '''
       conn = pymysql.connect(host = 'localhost', 
                            user = 'root', 
                            passwd = 'root', 
                            db = 'messages',
                            cursorclass=pymysql.cursors.DictCursor)
       
       try:
           with conn.cursor() as cur:
             cur.execute('select * from messages where id = %s', id)
             result = cur.fetchall()
             print(result)
             return jsonify({'message': result})
       finally:
           conn.close()
       return jsonify({'Error': result})
       
    ##################################################################
    def delete(self, id):
       ''' remove record from MySql database messages '''
       conn = pymysql.connect(host = 'localhost', 
                            user = 'root', 
                            passwd = 'root', 
                            db = 'messages',
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
             else:
                 print("ERROR: message table was not update")
                 result = {'numofrecs':0}
       finally:
           conn.close()
       return jsonify({'message': result})
       
    #################################################################
    def put(self, id):
       ''' Update records in MySql database messages '''
       conn = pymysql.connect(host = 'localhost', 
                            user = 'root', 
                            passwd = 'root', 
                            db = 'messages',
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
                 print("ERROR: message table was not update")
                 result = {'numofrecs':0}
       finally:
           conn.close()
       return jsonify({'message': result})
       
       
    #################################################################
    # testing with requests:
    # requests.post('http://127.0.0.1/id/6', \
    #          data={"route":value1, "message":msg}).json()   
    def post(self, id):
       ''' Insert records in MySql database messages from rabbitmq '''
       conn = pymysql.connect(host = 'localhost', 
                            user = 'root', 
                            passwd = 'root', 
                            db = 'messages',
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
             if not recr:
                 result = {'numofrecs':recr}
             else:
                 result = {'numofrecs':0}
       finally:
           conn.close()
       return jsonify({'message': result})

#####################################################################       
api.add_resource(Message, '/id/<string:id>')  
    
if __name__ == '__main__':
  app.run(debug = True)